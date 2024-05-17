from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class DetailForm(FlaskForm):
    description = StringField("description")
    user_id = IntegerField("user_id")
    company_id = IntegerField("company_id")
    submit = SubmitField("Submit")
