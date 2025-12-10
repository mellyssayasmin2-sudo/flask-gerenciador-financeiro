import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # IMPORTAR ROTAS AQUI
    from src.routes.auth import auth_routes
    from src.routes.expenses import expense_routes

    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(expense_routes, url_prefix="")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Render injeta a porta aqui
    app.run(host="0.0.0.0", port=port)
