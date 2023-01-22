from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
    picture = FileField('File Gambar', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    gallery = SelectField('Kategori Galeri', coerce=int)
    description = StringField('Deskripsi', validators=[DataRequired()])
    submit = SubmitField('Simpan Gambar')

class GalleryForm(FlaskForm):
    title = StringField('Nama Galeri', validators=[DataRequired()])
    submit = SubmitField('Simpan Galeri')