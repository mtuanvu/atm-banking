from passlib.context import CryptContext
import mysql.connector
from config import get_db_connection

# Khởi tạo pwd_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    hashed_password = pwd_context.hash(password)

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError as ie:
        print(f"IntegrityError: {ie}")  # Handle integrity error (e.g., duplicate email)
        return False
    except Exception as e:
        print(f"Error: {e}")  # Handle other errors
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and pwd_context.verify(password, user['password']):
        return "Login successful"
    else:
        return "Invalid email or password"

def change_password(email: str, old_password: str, new_password: str) -> bool:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Lấy người dùng từ cơ sở dữ liệu
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    # Kiểm tra mật khẩu cũ và cập nhật mật khẩu mới
    if user and pwd_context.verify(old_password, user['password']):  # Kiểm tra mật khẩu cũ
        hashed_new_password = pwd_context.hash(new_password)  # Mã hóa mật khẩu mới
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_new_password, email))
        connection.commit()
        return True

    return False