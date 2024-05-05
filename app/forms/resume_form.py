from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class ResumeForm(FlaskForm):
    user_id = IntegerField("tour_id")
    name = StringField("name")
    submit = SubmitField("Submit")
