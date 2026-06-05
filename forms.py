from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=255)])
    password2 = PasswordField(
        "Konfirmasi Password",
        validators=[DataRequired(), EqualTo("password", message="Password tidak sama")],
    )

    submit = SubmitField("Daftar")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])

    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    telepon = StringField("Nomor Telepon", validators=[DataRequired(), Length(max=40)])
    pesan = TextAreaField("Pesan", validators=[DataRequired(), Length(max=5000)])

    submit = SubmitField("Kirim Pesan")


class TicketForm(FlaskForm):
    judul = StringField("Judul", validators=[DataRequired(), Length(max=180)])
    pesan = TextAreaField("Pesan", validators=[DataRequired(), Length(max=8000)])
    submit = SubmitField("Buat Tiket")


class TicketMessageForm(FlaskForm):
    pesan = TextAreaField("Pesan", validators=[DataRequired(), Length(max=8000)])
    submit = SubmitField("Kirim Balasan")


class OrderConfirmForm(FlaskForm):
    # Minimal sesuai struktur database
    submit = SubmitField("Konfirmasi Pesanan")


class CustomerOrderCancelForm(FlaskForm):
    submit = SubmitField("Batalkan Pesanan")


class CustomerTicketEditForm(FlaskForm):
    judul = StringField("Judul", validators=[DataRequired(), Length(max=180)])
    pesan = TextAreaField("Pesan", validators=[DataRequired(), Length(max=8000)])
    submit = SubmitField("Simpan Perubahan")


class CustomerTicketDeleteConfirmForm(FlaskForm):
    submit = SubmitField("Hapus Tiket")


class CustomerTicketCloseForm(FlaskForm):
    submit = SubmitField("Tutup Tiket (resolved)")


class AdminUserRoleEditForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    role = StringField("Role", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Simpan")


class AdminContactDeleteConfirmForm(FlaskForm):
    submit = SubmitField("Hapus Pesan")


class AdminPackageUpdateForm(FlaskForm):
    nama_paket = StringField("Nama Paket", validators=[DataRequired(), Length(max=120)])
    tipe = StringField("Tipe (shared/dedicated)", validators=[DataRequired(), Length(max=30)])
    harga = IntegerField("Harga (IDR/bulan)", validators=[DataRequired()])
    spesifikasi = TextAreaField("Spesifikasi", validators=[DataRequired(), Length(max=10000)])
    submit = SubmitField("Simpan")


class AdminTicketStatusForm(FlaskForm):
    status = StringField("Status", validators=[DataRequired(), Length(max=30)])
    pesan = TextAreaField("Balasan Admin", validators=[Optional(), Length(max=8000)])
    submit = SubmitField("Update Tiket")


class AdminOrderStatusForm(FlaskForm):
    status = StringField("Status Pesanan", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Update Order")


class AdminUserDeleteConfirmForm(FlaskForm):
    submit = SubmitField("Hapus User")

