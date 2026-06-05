from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import Mapped

from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    nama: Mapped[str] = db.Column(db.String(120), nullable=False)
    email: Mapped[str] = db.Column(db.String(180), unique=True, nullable=False)
    password_hash: Mapped[str] = db.Column(db.String(255), nullable=False)
    role: Mapped[str] = db.Column(db.String(20), default="customer", nullable=False)

    orders = db.relationship("Order", back_populates="user", lazy="dynamic")
    tickets = db.relationship("SupportTicket", back_populates="user", lazy="dynamic")
    ticket_messages = db.relationship("TicketMessage", back_populates="author", lazy="dynamic")


class HostingPackage(db.Model):
    __tablename__ = "hosting_packages"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    nama_paket: Mapped[str] = db.Column(db.String(120), nullable=False)
    tipe: Mapped[str] = db.Column(db.String(30), nullable=False)  # shared/dedicated
    harga: Mapped[int] = db.Column(db.Integer, nullable=False)  # in IDR
    spesifikasi: Mapped[str] = db.Column(db.Text, nullable=False)

    orders = db.relationship("Order", back_populates="package", lazy="dynamic")


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    package_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("hosting_packages.id"), nullable=False)

    tanggal_pesan: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[str] = db.Column(db.String(30), default="pending", nullable=False)

    user = db.relationship("User", back_populates="orders")
    package = db.relationship("HostingPackage", back_populates="orders")


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    nama: Mapped[str] = db.Column(db.String(120), nullable=False)
    email: Mapped[str] = db.Column(db.String(180), nullable=False)
    telepon: Mapped[str] = db.Column(db.String(40), nullable=False)
    pesan: Mapped[str] = db.Column(db.Text, nullable=False)

    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class SupportTicket(db.Model):
    __tablename__ = "support_tickets"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    judul: Mapped[str] = db.Column(db.String(180), nullable=False)
    pesan: Mapped[str] = db.Column(db.Text, nullable=False)
    status: Mapped[str] = db.Column(db.String(30), default="pending", nullable=False)

    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="tickets")
    messages = db.relationship("TicketMessage", back_populates="ticket", lazy="dynamic", cascade="all, delete-orphan")


class TicketMessage(db.Model):
    __tablename__ = "ticket_messages"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    ticket_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("support_tickets.id"), nullable=False)
    author_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    pesan: Mapped[str] = db.Column(db.Text, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    ticket = db.relationship("SupportTicket", back_populates="messages")
    author = db.relationship("User", back_populates="ticket_messages")

