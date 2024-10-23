from flask import Blueprint, request, jsonify
from models.TransactionModel import deposit_money, withdraw_money

transaction_bp = Blueprint('transaction_bp', __name__)

# Route nạp tiền
@transaction_bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    # Xử lý nạp tiền
    deposit_money(account_id, amount)

    return jsonify({"message": "Deposit successful!"})

# Route rút tiền
@transaction_bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    # Xử lý rút tiền
    new_balance = withdraw_money(account_id, amount)
    if new_balance is not None:
        return jsonify({"message": "Withdrawal successful!", "new_balance": new_balance})
    else:
        return jsonify({"error": "Insufficient balance!"}), 400
