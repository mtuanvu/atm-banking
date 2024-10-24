from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.AccountModel import get_account_by_user_id

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/info', methods=['GET'])
@jwt_required()
def get_account_info():
    user_id = get_jwt_identity()
    accounts = get_account_by_user_id(user_id)
    
    if accounts:
        return jsonify({
            "account_id": accounts['account_id'],
            "balance": accounts['balance']
        }), 200
    else:
        return jsonify({"error": "Account not found"}), 404
    