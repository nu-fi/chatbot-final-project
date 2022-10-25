from ast import Str
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TimeField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
# from wtforms_components import PhoneNumberField

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

class BerkasForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()], render_kw={"placeholder": "Nama Lengkap"})
    no_hp = StringField('No. HP', validators=[DataRequired()], render_kw={"placeholder": "No. Handphone"})
    alamat_praktik = StringField('Alamat Praktik', validators=[DataRequired()], render_kw={"placeholder": "Alamat Praktik"})
    tempat_praktik = StringField('Tempat Praktik', validators=[DataRequired()], render_kw={"placeholder": "Tempat Praktik"})

    # hari_praktik = SelectMultipleField('Hari Praktik', validators=[DataRequired()], choices=[], validate_choice=False)
    # hari_praktik = MultiCheckboxField('Hari Praktik', choices=[("Senin", "Senin"), ("Selasa", "Selasa"), ("Rabu", "Rabu"), ("Kamis", "Kamis"), ("Jumat", "Jumat"), ("Sabtu", "Sabtu"), ("Minggu", "Minggu")])

    jam_mulai = TimeField('Jam Mulai Praktik', format='%H:%M')
    jam_selesai = TimeField('Jam Selesai Praktik', format='%H:%M')
    kota_praktik = SelectField('Kabupaten/Kota Praktik', validate_choice=False, validators=[DataRequired()], render_kw={"placeholder": "Kota Praktik"}, choices=[('', 'Pilih Kota'), ("Kota Pontianak", "Kota Pontianak"), ("Kota Singkawang", "Kota Singkawang"), ("Kabupaten Bengkayang", "Kabupaten Bengkayang"), ("Kabupaten Kapuas Hulu", "Kabupaten Kapuas Hulu"), ("Kabupaten Kayong Utara", "Kabupaten Kayong Utara"), ("Kabupaten Ketapang", "Kabupaten Ketapang"), ("Kabupaten Kubu Raya", "Kabupaten Kubu Raya"), ("Kabupaten Landak", "Kabupaten Landak"), ("Kabupaten Melawi", "Kabupaten Melawi"), ("Kabupaten Mempawah", "Kabupaten Mempawah"), ("Kabupaten Sambas", "Kabupaten Sambas"), ("Kabupaten Sanggau", "Kabupaten Sanggau"), ("Kabupaten Sekadau", "Kabupaten Sekadau"), ("Kabupaten Sintang", "Kabupaten Sintang")])
    batas_sip = DateField('Terakhir Berlaku SIP', validators=[DataRequired()], format='%Y-%m-%d')
    
    file_sip = FileField('File SIP', validators=[FileAllowed(['pdf'])])
    file_ijazah = FileField('File Ijazah', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Simpan Data')
