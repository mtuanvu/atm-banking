from flask import Blueprint, request, jsonify
from models.UserModel import register_user, login_user, change_password  

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if register_user(name, email, password):
        return jsonify({"message": "User registered successfully."}), 201
    else:
        return jsonify({"error": "Registration failed."}), 400

@user_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = login_user(email, password)
    if result == "Login successful":
        return jsonify({"message": result}), 200
    else:
        return jsonify({"error": result}), 401


@user_bp.route('/user/change-password', methods=['POST'])
def change_password_route():
    data = request.json
    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if change_password(email, old_password, new_password):
        return jsonify({"message": "Password changed successfully!"}), 200
    else:
        return jsonify({"error": "Failed to change password. Check old password and try again."}), 400