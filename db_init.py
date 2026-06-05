"""Initialize database schema and seed data.

This app uses SQLAlchemy `db.create_all()` inside `create_app()`,
so calling `create_app()` once is enough to ensure tables and seed rows exist.

Run:
  python db_init.py
"""

from app_factory import create_app

app = create_app()

# Force app context to ensure create_all/seed executed
with app.app_context():
    pass

print("DB initialized/verified.")

