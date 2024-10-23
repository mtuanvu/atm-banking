# routes/TransactionRoute.py
from flask import Blueprint, request, jsonify
from models.TransactionModel import deposit_money, withdraw_money, transfer_money, get_transaction_history

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    deposit_money(account_id, amount)
    return jsonify({"message": "Deposit successful!"})

@transaction_bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    new_balance = withdraw_money(account_id, amount)
    if new_balance is not None:
        return jsonify({"message": "Withdrawal successful!", "new_balance": new_balance})
    else:
        return jsonify({"error": "Insufficient balance!"}), 400

@transaction_bp.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    from_account_id = data['from_account_id']
    to_account_id = data['to_account_id']
    amount = data['amount']
    # Chuyển tiền giữa các tài khoản
    result = transfer_money(from_account_id, to_account_id, amount)
    if result:
        return jsonify({"message": "Transfer successful!"})
    else:
        return jsonify({"error": "Transfer failed!"}), 400

@transaction_bp.route('/transactions', methods=['GET'])
def transactions():
    account_id = request.args.get('account_id')
    transactions = get_transaction_history(account_id)  # Lấy lịch sử giao dịch cho tài khoản cụ thể
    return jsonify({"transactions": transactions})