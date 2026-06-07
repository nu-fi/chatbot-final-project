from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, DateField, FieldList, FormField
from wtforms.validators import DataRequired

class TempatPraktikForm(FlaskForm):
    alamat_praktik = StringField('Alamat Praktik', validators=[DataRequired()], render_kw={"placeholder": "Alamat Praktik"})
    tempat_praktik = StringField('Tempat Praktik', validators=[DataRequired()], render_kw={"placeholder": "Tempat Praktik"})
    jam_mulai = TimeField('Jam Mulai Praktik', format='%H:%M', validators=[DataRequired()])
    jam_selesai = TimeField('Jam Selesai Praktik', format='%H:%M', validators=[DataRequired()])
    kota_praktik = SelectField('Kabupaten/Kota Praktik', validate_choice=False, validators=[DataRequired()], render_kw={"placeholder": "Kota Praktik"}, choices=[('', 'Pilih Kota'), ("Kota Pontianak", "Kota Pontianak"), ("Kota Singkawang", "Kota Singkawang"), ("Kabupaten Bengkayang", "Kabupaten Bengkayang"), ("Kabupaten Kapuas Hulu", "Kabupaten Kapuas Hulu"), ("Kabupaten Kayong Utara", "Kabupaten Kayong Utara"), ("Kabupaten Ketapang", "Kabupaten Ketapang"), ("Kabupaten Kubu Raya", "Kabupaten Kubu Raya"), ("Kabupaten Landak", "Kabupaten Landak"), ("Kabupaten Melawi", "Kabupaten Melawi"), ("Kabupaten Mempawah", "Kabupaten Mempawah"), ("Kabupaten Sambas", "Kabupaten Sambas"), ("Kabupaten Sanggau", "Kabupaten Sanggau"), ("Kabupaten Sekadau", "Kabupaten Sekadau"), ("Kabupaten Sintang", "Kabupaten Sintang")])
    submit = SubmitField('Simpan Data')

class BerkasForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()], render_kw={"placeholder": "Nama Lengkap"})
    no_hp = StringField('No. HP', validators=[DataRequired()], render_kw={"placeholder": "No. Handphone"})
    batas_sip = DateField('Terakhir Berlaku SIP', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('Simpan Data')