from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField("Nama", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subjek", validators=[DataRequired()])
    message = TextAreaField("Pesan", validators=[DataRequired()])
    submit = SubmitField("Kirim")

class SearchForm(FlaskForm):
    searched = StringField("Search Doctor by Name, Location...", validators=[DataRequired()])
    submit = SubmitField("Kirim")