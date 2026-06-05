from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from extensions import db
from forms import (
    OrderConfirmForm,
    TicketForm,
    TicketMessageForm,
    ContactForm,
    CustomerOrderCancelForm,
    CustomerTicketEditForm,
    CustomerTicketDeleteConfirmForm,
    CustomerTicketCloseForm,
)


from models import HostingPackage, Order, SupportTicket, TicketMessage, ContactMessage

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/dashboard")
@login_required
def dashboard():
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.tanggal_pesan.desc())
        .all()
    )
    tickets = (
        SupportTicket.query.filter_by(user_id=current_user.id)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
    return render_template("customer/dashboard.html", orders=orders, tickets=tickets)


@customer_bp.route("/orders")
@login_required
def orders():
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.tanggal_pesan.desc())
        .all()
    )
    return render_template("customer/orders.html", orders=orders)


@customer_bp.route("/paket/order/<int:package_id>", methods=["GET", "POST"])
@login_required
def order_package(package_id: int):
    package = HostingPackage.query.get_or_404(package_id)
    form = OrderConfirmForm()
    if form.validate_on_submit():
        order = Order(user_id=current_user.id, package_id=package.id, status="pending")
        db.session.add(order)
        db.session.commit()
        flash("Pesanan berhasil dibuat. Status: pending", "success")
        return redirect(url_for("customer.orders"))

    return render_template("customer/order_confirm.html", package=package, form=form)


@customer_bp.route("/tickets")
@login_required
def tickets():
    tickets = (
        SupportTicket.query.filter_by(user_id=current_user.id)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
    return render_template("customer/tickets.html", tickets=tickets)


@customer_bp.route("/tickets/buat", methods=["GET", "POST"])
@login_required
def ticket_create():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = SupportTicket(
            user_id=current_user.id,
            judul=form.judul.data.strip(),
            pesan=form.pesan.data.strip(),
            status="pending",
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Tiket berhasil dibuat.", "success")
        return redirect(url_for("customer.tickets"))

    return render_template("customer/ticket_create.html", form=form)


@customer_bp.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticket_detail(ticket_id: int):
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=current_user.id).first_or_404()
    form = TicketMessageForm()
    if form.validate_on_submit():
        msg = TicketMessage(ticket_id=ticket.id, author_id=current_user.id, pesan=form.pesan.data.strip())
        db.session.add(msg)
        db.session.commit()
        flash("Pesan terkirim.", "success")
        return redirect(url_for("customer.ticket_detail", ticket_id=ticket.id))

    messages = ticket.messages.order_by(TicketMessage.created_at.asc()).all()
    return render_template("customer/ticket_detail.html", ticket=ticket, messages=messages, form=form)


@customer_bp.route("/orders/<int:order_id>/cancel", methods=["GET", "POST"])
@login_required
def order_cancel(order_id: int):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    form = CustomerOrderCancelForm()
    if form.validate_on_submit():
        order.status = "canceled"
        db.session.commit()
        flash("Order dibatalkan.", "info")
        return redirect(url_for("customer.orders"))
    return render_template("customer/order_cancel.html", order=order, form=form)


@customer_bp.route("/tickets/<int:ticket_id>/edit", methods=["GET", "POST"])
@login_required
def ticket_edit(ticket_id: int):
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=current_user.id).first_or_404()
    form = CustomerTicketEditForm(obj=ticket)
    if form.validate_on_submit():
        ticket.judul = form.judul.data.strip()
        ticket.pesan = form.pesan.data.strip()
        db.session.commit()
        flash("Tiket diperbarui.", "success")
        return redirect(url_for("customer.tickets"))
    return render_template("customer/ticket_edit.html", ticket=ticket, form=form)


@customer_bp.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
@login_required
def ticket_delete(ticket_id: int):
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=current_user.id).first_or_404()
    form = CustomerTicketDeleteConfirmForm()
    if form.validate_on_submit():
        db.session.delete(ticket)
        db.session.commit()
        flash("Tiket dihapus.", "info")
    return redirect(url_for("customer.tickets"))


@customer_bp.route("/tickets/<int:ticket_id>/close", methods=["POST"])
@login_required
def ticket_close(ticket_id: int):
    ticket = SupportTicket.query.filter_by(id=ticket_id, user_id=current_user.id).first_or_404()
    form = CustomerTicketCloseForm()
    if form.validate_on_submit():
        ticket.status = "resolved"
        db.session.commit()
        flash("Tiket ditutup (resolved).", "success")
    return redirect(url_for("customer.tickets"))


@customer_bp.route("/kontak", methods=["GET", "POST"])
def contact():

    # Public page but save to DB
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            nama=form.nama.data.strip(),
            email=form.email.data.strip().lower(),
            telepon=form.telepon.data.strip(),
            pesan=form.pesan.data.strip(),
        )
        db.session.add(msg)
        db.session.commit()
        flash("Pesan terkirim. Terima kasih!", "success")
        return redirect(url_for("public.home"))

    return render_template("public/contact.html", form=form)


