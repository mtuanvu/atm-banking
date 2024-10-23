from config import get_db_connection

def deposit_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Nạp tiền vào tài khoản
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
    
    # Ghi lại giao dịch
    cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'deposit', %s)", (account_id, amount))

    conn.commit()
    cursor.close()
    conn.close()

def withdraw_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Kiểm tra số dư tài khoản
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    account = cursor.fetchone()

    if account and account['balance'] >= amount:
        new_balance = account['balance'] - amount
        
        # Cập nhật số dư mới
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
        
        # Ghi lại giao dịch
        cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'withdraw', %s)", (account_id, amount))

        conn.commit()
        cursor.close()
        conn.close()

        return new_balance
    
    cursor.close()
    conn.close()
    return None
