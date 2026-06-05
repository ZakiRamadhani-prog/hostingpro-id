from flask import Blueprint, render_template

public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    return render_template("public/home.html")


@public_bp.get("/shared-hosting")
def shared_hosting():
    return render_template("public/shared.html")


@public_bp.get("/dedicated-server")
def dedicated_server():
    return render_template("public/dedicated.html")


@public_bp.get("/tentang")
def about():
    return render_template("public/about.html")


@public_bp.get("/faq")
def faq():
    return render_template("public/faq.html")


