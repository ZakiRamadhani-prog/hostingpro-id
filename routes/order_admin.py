from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from extensions import db
from forms import AdminOrderStatusForm
from models import Order

admin_order_bp = Blueprint("admin_orders", __name__)


def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


@admin_order_bp.route("/orders")
@login_required
def list_orders():
    admin_required()
    orders = Order.query.order_by(Order.tanggal_pesan.desc()).all()
    return render_template("admin/orders.html", orders=orders)


@admin_order_bp.route("/orders/<int:order_id>", methods=["GET", "POST"])
@login_required
def order_detail(order_id: int):
    admin_required()
    order = Order.query.get_or_404(order_id)

    form = AdminOrderStatusForm(status=order.status)
    if form.validate_on_submit():
        order.status = form.status.data.strip()
        db.session.commit()
        flash("Status order diperbarui.", "success")
        return redirect(url_for("admin_orders.order_detail", order_id=order.id))

    return render_template("admin/order_detail.html", order=order, form=form)

