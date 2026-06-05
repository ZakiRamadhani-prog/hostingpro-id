import os

from flask import Flask

from extensions import db, login_manager, csrf
from config import Config
from models import User, HostingPackage


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load config
    config_class = config_class or Config
    app.config.from_object(config_class)

    # Ensure instance-relative folders exist if used
    os.makedirs(app.config.get("SQLALCHEMY_DATABASE_URI"), exist_ok=True) if False else None

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from routes.public import public_bp
    from routes.auth import auth_bp
    from routes.customer import customer_bp
    from routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # customer_bp memuat endpoint login-required dan juga contact publik (/kontak)
    app.register_blueprint(customer_bp)

    # Admin
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Admin orders processing
    from routes.order_admin import admin_order_bp
    app.register_blueprint(admin_order_bp, url_prefix="/admin")



    # Create tables + seed
    with app.app_context():
        db.create_all()

        # Seed packages if empty
        if HostingPackage.query.count() == 0:
            seed_packages()
        if User.query.count() == 0:
            seed_users()

    return app


def seed_packages() -> None:
    from models import HostingPackage

    packages = [
        {
            "nama_paket": "Basic",
            "tipe": "shared",
            "harga": 25000,
            "spesifikasi": "1 Website\n10 GB SSD\nFree SSL",
        },
        {
            "nama_paket": "Business",
            "tipe": "shared",
            "harga": 75000,
            "spesifikasi": "10 Website\n50 GB SSD\nFree SSL\nDaily Backup",
        },
        {
            "nama_paket": "Premium",
            "tipe": "shared",
            "harga": 150000,
            "spesifikasi": "Unlimited Website\n100 GB SSD\nFree SSL\nDaily Backup\nPriority Support",
        },
        {
            "nama_paket": "Starter Server",
            "tipe": "dedicated",
            "harga": 1500000,
            "spesifikasi": "CPU 4 Core\nRAM 8 GB\nSSD 240 GB",
        },
        {
            "nama_paket": "Professional Server",
            "tipe": "dedicated",
            "harga": 3000000,
            "spesifikasi": "CPU 8 Core\nRAM 16 GB\nSSD 480 GB",
        },
        {
            "nama_paket": "Enterprise Server",
            "tipe": "dedicated",
            "harga": 6000000,
            "spesifikasi": "CPU 16 Core\nRAM 32 GB\nSSD 1 TB",
        },
    ]

    for p in packages:
        db.session.add(HostingPackage(**p))
    db.session.commit()


def seed_users() -> None:
    from werkzeug.security import generate_password_hash
    from models import User

    # Admin default
    admin = User(
        nama="Admin",
        email="admin@example.com",
        password_hash=generate_password_hash("admin123"),
        role="admin",
    )

    customer = User(
        nama="Demo Customer",
        email="customer@example.com",
        password_hash=generate_password_hash("customer123"),
        role="customer",
    )

    db.session.add(admin)
    db.session.add(customer)
    db.session.commit()

