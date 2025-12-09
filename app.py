from flask import Flask 
from src.db import db
from src.routes.expenses import expense_routes
from src.routes.auth import auth_routes
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(expense_routes)
    app.register_blueprint(auth_routes)

    return app

app = create_app()
