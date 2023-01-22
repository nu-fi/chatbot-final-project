from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FilesForm(FlaskForm):
    title = StringField('Nama Berkas', validators=[DataRequired()])
    description = StringField('Deskripsi Berkas', validators=[DataRequired()])
    file = FileField('Berkas', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx', 'xlsx', 'csv'])])
    submit = SubmitField('Simpan File')
    

