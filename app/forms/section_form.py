from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class SectionForm(FlaskForm):
    title = StringField("title")
    resume_id = IntegerField("resume_id")
    submit = SubmitField("Submit")
