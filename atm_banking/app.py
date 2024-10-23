from flask import Flask
from routes.UserRoute import user_bp
from routes.TransactionRoute import transaction_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
