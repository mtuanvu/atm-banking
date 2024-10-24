from passlib.context import CryptContext
import mysql.connector
from config import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(name, email, password, account_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    hashed_password = pwd_context.hash(password)

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        conn.commit()

        # Tạo account cho user
        cursor.execute("INSERT INTO accounts (account_id, user_id, balance) VALUES (%s, %s, 0)", (account_id, cursor.lastrowid))
        conn.commit()

        return True, "User registered successfully."
    except mysql.connector.IntegrityError as ie:
        return False, f"IntegrityError: {ie}"  # Handle integrity error (e.g., duplicate email or account_id)
    except Exception as e:
        return False, f"Error: {e}"
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and pwd_context.verify(old_password, user['password']):
        hashed_new_password = pwd_context.hash(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_new_password, email))
        conn.commit()
        return True

    return False
