from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class ArticleForm(FlaskForm):
    title = StringField('Judul Artikel', validators=[DataRequired()], render_kw={"placeholder": "Judul Artikel"})
    content = CKEditorField('Isi Artikel', validators=[DataRequired()])
    picture = FileField('Gambar Artikel', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Kategori', coerce=int)
    submit = SubmitField('Simpan Artikel')

class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()], render_kw={"placeholder": "Nama Kategori"})
    submit = SubmitField('Simpan Kategori')
