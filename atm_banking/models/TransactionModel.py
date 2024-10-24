import mysql.connector
from config import get_db_connection


def deposit_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra xem tài khoản có tồn tại hay không
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return False, "Account does not exist"

    try:
        query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
        cursor.execute(query, (amount, account_id))

        # Thêm vào bảng giao dịch
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'deposit', %s)",
            (account_id, amount),
        )
        conn.commit()

        cursor.close()
        conn.close()
        return True, "Deposit successful"
    except Exception as e:
        conn.rollback()
        print(f"Error during deposit: {e}")
        cursor.close()
        conn.close()
        return False, "Deposit failed"


def withdraw_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra tài khoản tồn tại
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()

    if balance is None:
        cursor.close()
        conn.close()
        return None, "Account does not exist"

    # Chuyển đổi amount thành kiểu số (integer)
    amount = int(amount)

    # Kiểm tra số dư có đủ không
    if balance[0] >= amount:
        try:
            query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            cursor.execute(query, (amount, account_id))

            # Thêm giao dịch vào bảng transactions
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'withdraw', %s)",
                (account_id, amount),
            )
            conn.commit()

            cursor.close()
            conn.close()
            return balance[0] - amount, "Withdrawal successful"
        except Exception as e:
            conn.rollback()
            print(f"Error during withdrawal: {e}")
            cursor.close()
            conn.close()
            return None, "Withdrawal failed due to server error"
    else:
        cursor.close()
        conn.close()
        return None, "Insufficient balance"


def transfer_money(from_account_id, to_account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra tài khoản gửi
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,)
    )
    from_balance = cursor.fetchone()

    if from_balance is None:
        cursor.close()
        conn.close()
        return False, "Sender account does not exist"

    # Kiểm tra tài khoản nhận
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_id = %s", (to_account_id,)
    )
    to_balance = cursor.fetchone()

    if to_balance is None:
        cursor.close()
        conn.close()
        return False, "Recipient account does not exist"

    if from_balance[0] >= amount:
        try:
            # Trừ tiền tài khoản gửi
            cursor.execute(
                "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
                (amount, from_account_id),
            )

            # Cộng tiền tài khoản nhận
            cursor.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
                (amount, to_account_id),
            )

            # Ghi lại giao dịch cho cả 2 tài khoản
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer', %s)",
                (from_account_id, amount),
            )
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer', %s)",
                (to_account_id, amount),
            )

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Transfer successful"
        except Exception as e:
            conn.rollback()
            print(f"Error during transfer: {e}")
            cursor.close()
            conn.close()
            return False, "Transfer failed"
    else:
        cursor.close()
        conn.close()
        return False, "Insufficient balance"


def get_account_info_and_user_name(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lấy user_id từ bảng accounts dựa trên account_id
    cursor.execute("SELECT user_id FROM accounts WHERE account_id = %s", (account_id,))
    account_info = cursor.fetchone()

    if account_info:
        user_id = account_info[0]
        
        # Lấy tên người dùng từ bảng users dựa trên user_id
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_info:
            return {
                "account_id": account_id,
                "user_id": user_id,
                "user_name": user_info[0]  # Cột tên trong bảng users
            }
    cursor.close()
    conn.close()
    return None



def get_transaction_history(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transactions WHERE account_id = %s ORDER BY date DESC"
    cursor.execute(query, (account_id,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "id": t[0],
            "account_id": t[1],
            "transaction_type": t[2],
            "amount": t[3],
            "date": t[4],
        }
        for t in transactions
    ]
