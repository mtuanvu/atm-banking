import mysql.connector
from config import get_db_connection
import datetime
from decimal import Decimal


def deposit_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return False, "Account does not exist"

    try:
        query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
        cursor.execute(query, (amount, account_id))

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


#han mucimport decimal
def check_withdrawal_limit(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lấy tổng số tiền đã rút trong ngày
    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE account_id = %s AND transaction_type = 'withdraw' AND DATE(date) = CURDATE()",
        (account_id,)
    )
    total_withdrawn_today = cursor.fetchone()[0] or Decimal(0)

    cursor.close()
    conn.close()

    # Giới hạn rút tiền trong một ngày là 50 triệu
    limit = Decimal(50000000)

    # Đảm bảo amount cũng là kiểu Decimal để tính toán
    amount = Decimal(amount)

    if total_withdrawn_today + amount > limit:
        return False, total_withdrawn_today
    else:
        return True, total_withdrawn_today


def check_transfer_limit(amount):
    limit = 10000000  # Hạn mức chuyển tiền trong một lần
    amount = float(amount)  # Chuyển đổi 'amount' về dạng số
    return amount <= limit


def withdraw_money(account_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra giới hạn rút tiền
    is_within_limit, total_withdrawn_today = check_withdrawal_limit(account_id, amount)
    if not is_within_limit:
        cursor.close()
        conn.close()
        return None, "Exceeded daily withdrawal limit"

    # Lấy số dư tài khoản
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()

    if balance is None:
        cursor.close()
        conn.close()
        return None, "Account does not exist"

    amount = Decimal(amount)

    if balance[0] >= amount:
        try:
            query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            cursor.execute(query, (amount, account_id))

            # Ghi giao dịch rút tiền vào bảng transactions
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

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
    from_balance = cursor.fetchone()

    if from_balance is None:
        cursor.close()
        conn.close()
        return False, "Sender account does not exist"

    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (to_account_id,))
    to_balance = cursor.fetchone()

    if to_balance is None:
        cursor.close()
        conn.close()
        return False, "Recipient account does not exist"

    amount = float(amount)

    # Kiểm tra hạn mức chuyển tiền
    is_within_limit = check_transfer_limit(amount)
    if not is_within_limit:
        return False, "Transfer limit exceeded."

    if from_balance[0] >= amount:
        try:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account_id))

            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer', %s)", (from_account_id, amount))
            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer', %s)", (to_account_id, amount))

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



#check accountid
def get_account_info_and_user_name(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM accounts WHERE account_id = %s", (account_id,))
    account_info = cursor.fetchone()

    if account_info:
        user_id = account_info[0]
        
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_info:
            return {
                "account_id": account_id,
                "user_id": user_id,
                "user_name": user_info[0] 
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
            "account_id": t[1],
            "transaction_type": t[2],
            "amount": t[3],
            "date": t[4],
        }
        for t in transactions
    ]