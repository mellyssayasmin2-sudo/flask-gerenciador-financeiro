import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    from src.routes.auth import auth_routes
    from src.routes.expenses import expense_routes

    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(expense_routes)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
