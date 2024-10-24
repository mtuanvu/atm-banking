import mysql.connector
from config import get_db_connection

def get_account_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT account_id, balance FROM accounts WHERE user_id = %s", (user_id,))
    account = cursor.fetchone()

    if account:
        print(f"Account found: {account}")
        return {
            "account_id": account[0],
            "balance": account[1]
        }
    else:
        print(f"No account found for user_id: {user_id}")
        return None

