from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class NewsForm(FlaskForm):
    title = StringField('Judul Berita', validators=[DataRequired()], render_kw={"placeholder": "Judul Berita"})
    content = CKEditorField('Isi Berita', validators=[DataRequired()])
    picture = FileField('Gambar Berita', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Kategori', coerce=int)
    submit = SubmitField('Simpan Berita')

class CategoryForm(FlaskForm):
    name = StringField('Kategori Berita', validators=[DataRequired()], render_kw={"placeholder": "Nama Kategori"})
    submit = SubmitField('Simpan Kategori')