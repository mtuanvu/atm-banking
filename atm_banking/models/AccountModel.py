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

def get_account_ids_by_user_id(user_id):
    conn = get_db_connection() 
    cursor = conn.cursor()

    query = "SELECT account_id FROM accounts WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    account_ids = cursor.fetchall()

    cursor.close()
    conn.close()

    return [account[0] for account in account_ids]