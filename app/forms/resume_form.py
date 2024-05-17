from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class ResumeForm(FlaskForm):
    user_id = IntegerField("user_id")
    title = StringField("title")
    submit = SubmitField("Submit")
