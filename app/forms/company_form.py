from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class CompanyForm(FlaskForm):
    organization = StringField("organization")
    title = StringField("title")
    user_id = IntegerField("user_id")
    section_id = IntegerField("section_id")
    start_date = StringField("start_date")
    end_date = StringField("end_date")
    submit = SubmitField("Submit")
