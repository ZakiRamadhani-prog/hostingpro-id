from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id: str):
    # Import locally to avoid circular imports
    from models import User

    try:
        return User.query.get(int(user_id))
    except Exception:
        return None

