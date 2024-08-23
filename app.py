from flask import Flask
from config import Config
from models import db
from routes import chores_bp, transactions_bp
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register the routes
app.register_blueprint(chores_bp)
app.register_blueprint(transactions_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)