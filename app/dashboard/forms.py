from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, URL, Optional


class LinkForm(FlaskForm):
    platform = StringField('Platform', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])


class CardForm(FlaskForm):
    brand_name = StringField('Brand Name', validators=[DataRequired()])
    tagline = StringField('Tagline', validators=[Optional()])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Save Card')
