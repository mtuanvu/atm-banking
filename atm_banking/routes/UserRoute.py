from flask import Blueprint, request, jsonify
from models.UserModel import register_user, login_user

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
