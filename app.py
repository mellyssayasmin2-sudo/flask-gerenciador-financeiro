import os
from flask import Flask
from src.db import db
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from src.routes.auth import auth_routes
    from src.routes.expenses import expense_routes

    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(expense_routes)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
