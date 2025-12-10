from app import create_app

app = create_app()

with app.app_context():
    from src.db import db
    db.create_all()
