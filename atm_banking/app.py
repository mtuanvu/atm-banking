from flask import Flask
from flask_jwt_extended import JWTManager
from routes.UserRoute import user_bp
from routes.TransactionRoute import transaction_bp
from routes.AccountRoute import account_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['JWT_SECRET_KEY'] = '58983823111c66efa274fa874863b33f9a7fe5d243f631fed8a1933db799d1f5'

jwt = JWTManager(app)

# Đăng ký các route
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(account_bp, url_prefix='/account')

if __name__ == '__main__':
    app.run(debug=True)
