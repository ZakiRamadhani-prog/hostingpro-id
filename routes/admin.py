from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from extensions import db
from forms import AdminPackageUpdateForm, AdminTicketStatusForm, TicketMessageForm
from models import HostingPackage, User, ContactMessage, SupportTicket, TicketMessage

admin_bp = Blueprint("admin", __name__)


def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    admin_required()
    users_count = User.query.count()
    tickets_pending = SupportTicket.query.filter_by(status="pending").count()
    contacts_count = ContactMessage.query.count()
    # orders_count
    try:
        from models import Order

        orders_count = Order.query.count()
    except Exception:
        orders_count = 0


    return render_template(
        "admin/dashboard.html",
        users_count=users_count,
        tickets_pending=tickets_pending,
        contacts_count=contacts_count,
        orders_count=orders_count,
    )


@admin_bp.route("/paket")
@login_required
def packages():
    admin_required()
    packages = HostingPackage.query.order_by(HostingPackage.tipe.asc(), HostingPackage.harga.asc()).all()
    return render_template("admin/packages.html", packages=packages)


@admin_bp.route("/paket/tambah", methods=["GET", "POST"])
@login_required
def package_create():
    admin_required()
    form = AdminPackageUpdateForm()
    if form.validate_on_submit():
        pkg = HostingPackage(
            nama_paket=form.nama_paket.data.strip(),
            tipe=form.tipe.data.strip(),
            harga=form.harga.data,
            spesifikasi=form.spesifikasi.data.strip(),
        )
        db.session.add(pkg)
        db.session.commit()
        flash("Paket ditambahkan.", "success")
        return redirect(url_for("admin.packages"))

    return render_template("admin/package_form.html", form=form, mode="create")


@admin_bp.route("/paket/<int:package_id>/edit", methods=["GET", "POST"])
@login_required
def package_edit(package_id: int):
    admin_required()
    pkg = HostingPackage.query.get_or_404(package_id)
    form = AdminPackageUpdateForm(obj=pkg)
    if form.validate_on_submit():
        pkg.nama_paket = form.nama_paket.data.strip()
        pkg.tipe = form.tipe.data.strip()
        pkg.harga = form.harga.data
        pkg.spesifikasi = form.spesifikasi.data.strip()
        db.session.commit()
        flash("Paket diperbarui.", "success")
        return redirect(url_for("admin.packages"))

    return render_template("admin/package_form.html", form=form, mode="edit")


@admin_bp.route("/paket/<int:package_id>/hapus", methods=["POST"])
@login_required
def package_delete(package_id: int):
    admin_required()
    pkg = HostingPackage.query.get_or_404(package_id)
    db.session.delete(pkg)
    db.session.commit()
    flash("Paket dihapus.", "info")
    return redirect(url_for("admin.packages"))


@admin_bp.route("/pelanggan")
@login_required
def customers():
    admin_required()
    customers = User.query.filter_by(role="customer").order_by(User.id.desc()).all()
    return render_template("admin/customers.html", customers=customers)


@admin_bp.route("/kontak")
@login_required
def contacts():
    admin_required()
    contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/contacts.html", contacts=contacts)


@admin_bp.route("/tickets")
@login_required
def tickets():
    admin_required()
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template("admin/tickets.html", tickets=tickets)


@admin_bp.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id: int):
    admin_required()
    ticket = SupportTicket.query.get_or_404(ticket_id)

    form = AdminTicketStatusForm()
    if form.validate_on_submit():
        ticket.status = form.status.data.strip()
        db.session.commit()

        if form.pesan.data and form.pesan.data.strip():
            msg = TicketMessage(ticket_id=ticket.id, author_id=current_user.id, pesan=form.pesan.data.strip())
            db.session.add(msg)
            db.session.commit()

        flash("Tiket diperbarui.", "success")
        return redirect(url_for("admin.ticket_detail", ticket_id=ticket.id))

    messages = ticket.messages.order_by(TicketMessage.created_at.asc()).all()
    return render_template("admin/ticket_detail.html", ticket=ticket, messages=messages, form=form)

