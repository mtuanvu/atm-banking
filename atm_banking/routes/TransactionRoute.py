from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.TransactionModel import deposit_money, withdraw_money, transfer_money, get_transaction_history, get_account_info_and_user_name
from models.AccountModel import get_account_ids_by_user_id


transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    deposit_money(account_id, amount)
    return jsonify({"message": "Deposit successful!"})

@transaction_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    new_balance, message = withdraw_money(account_id, amount)
    if new_balance is not None:
        return jsonify({"message": message, "new_balance": new_balance}), 200
    else:
        return jsonify({"error": message}), 400

@transaction_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    data = request.json
    from_account_id = data.get('from_account_id')
    account_id = data.get('account_id')
    amount = data.get('amount')

    if not from_account_id or not account_id or not amount:
        return jsonify({"error": "Missing account or amount"}), 400

    result, message = transfer_money(from_account_id, account_id, amount)
    if result:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
    
    
@transaction_bp.route('/check_receiver', methods=['POST'])
@jwt_required()
def check_receiver():
    data = request.json
    account_id = data.get("account_id")

    # Gọi hàm từ Model để lấy thông tin tài khoản và tên người dùng
    account_info = get_account_info_and_user_name(account_id)

    if account_info:
        return jsonify({
            "message": "Tài khoản tồn tại",
            "receiver_name": account_info["user_name"]
        }), 200
    else:
        return jsonify({"error": "Tài khoản không tồn tại"}), 404


@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    user_id = get_jwt_identity()
    account_ids = get_account_ids_by_user_id(user_id)

    transactions = []
    for account_id in account_ids:
         transactions += get_transaction_history(account_id)

    return jsonify({"transactions": transactions})
