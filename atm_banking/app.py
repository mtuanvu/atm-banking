from flask import Flask
from flask_cors import CORS
from routes.UserRoute import user_bp
from routes.TransactionRoute import transaction_bp

app = Flask(__name__)
CORS(app)  # Cho phép CORS cho ứng dụng Flask

# Đăng ký blueprint cho routes
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
