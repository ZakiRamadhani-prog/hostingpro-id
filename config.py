import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///hosting_app.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Login
    LOGIN_VIEW = "auth.login"

    # Flask-WTF
    WTF_CSRF_TIME_LIMIT = None

