"""Initialize database schema and seed data.

Untuk deploy/hosting (mis. PythonAnywhere), Jalankan sekali setelah
mengatur DATABASE_URL.

Run:
  python db_init.py
"""

from app_factory import create_app

app = create_app()

with app.app_context():
    # create_all + seed already happens inside create_app()
    pass

print("DB initialized/verified.")

