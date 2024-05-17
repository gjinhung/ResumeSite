from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class TagForm(FlaskForm):
    tag = StringField("tag")
    user_id = IntegerField("user_id")
    submit = SubmitField("Submit")
