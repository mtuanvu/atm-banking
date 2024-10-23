import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_db_connection

def register_user(name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    hashed_password = generate_password_hash(password)  # Mã hóa mật khẩu

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError as ie:
        print(f"IntegrityError: {ie}")  # Xử lý lỗi
        return False
    except Exception as e:
        print(f"Error: {e}")  # Xử lý lỗi khác
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        return "Login successful"
    else:
        return "Invalid email or password"

