from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.UserModel import register_user, login_user, change_password  

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    account_id = data.get('account_id')

    # Kiểm tra dữ liệu đầu vào
    if not name or not email or not password or not account_id:
        return jsonify({"error": "All fields are required."}), 400

    if len(account_id) < 10:
        return jsonify({"error": "Account ID must be at least 10 characters long."}), 400

    success, message = register_user(name, email, password, account_id)
    if success:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"error": message}), 400


@user_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Kiểm tra dữ liệu đầu vào
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    result = login_user(email, password)
    if result == "Login successful":
        # Tạo JWT token khi đăng nhập thành công
        access_token = create_access_token(identity=email)
        return jsonify({"message": result, "token": access_token}), 200
    else:
        return jsonify({"error": result}), 401


@user_bp.route('/user/change-password', methods=['POST'])
@jwt_required()
def change_password_route():
    data = request.get_json()
    email = get_jwt_identity()  # Lấy email từ JWT token đã được xác thực
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # Kiểm tra dữ liệu đầu vào
    if not old_password or not new_password:
        return jsonify({"error": "Old password and new password are required."}), 400

    if change_password(email, old_password, new_password):
        return jsonify({"message": "Password changed successfully!"}), 200
    else:
        return jsonify({"error": "Failed to change password. Check old password and try again."}), 400


@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def profile():
    email = get_jwt_identity()  # Lấy email từ JWT token đã được xác thực
    return jsonify({"message": f"Welcome, {email}!"})
