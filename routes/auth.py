from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User
from forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("customer.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing:
            flash("Email sudah terdaftar.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(
            nama=form.nama.data.strip(),
            email=form.email.data.strip().lower(),
            password_hash=generate_password_hash(form.password.data),
            role="customer",
        )
        db.session.add(user)
        db.session.commit()
        flash("Registrasi berhasil. Silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # role-based
        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("customer.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash("Email atau password salah.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user)
        flash("Login berhasil.", "success")
        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("customer.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("public.home"))

