import mysql.connector
from config import get_db_connection


def deposit_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
    cursor.execute(query, (amount, account_id))
    conn.commit()
    cursor.close()
    conn.close()

def withdraw_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Kiểm tra số dư trước khi rút tiền
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
        cursor.execute(query, (amount, account_id))
        conn.commit()
        new_balance = balance - amount
        cursor.close()
        conn.close()
        return new_balance
    else:
        cursor.close()
        conn.close()
        return None  # Hoặc bạn có thể raise exception

def transfer_money(from_account_id, to_account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra số dư trước khi chuyển tiền
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
    from_balance = cursor.fetchone()[0]

    if from_balance >= amount:
        # Rút tiền từ tài khoản gửi
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account_id))
        # Nạp tiền vào tài khoản nhận
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False  # Hoặc bạn có thể raise exception

def get_transaction_history(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transactions WHERE account_id = %s ORDER BY date DESC"
    cursor.execute(query, (account_id,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": t[0], "account_id": t[1], "transaction_type": t[2], "amount": t[3], "date": t[4]} for t in transactions]
