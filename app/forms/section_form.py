from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from app.models import User


class SectionForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    user_id = IntegerField("user_id", validators=[DataRequired()])
    resume_id = IntegerField("resume_id", validators=[DataRequired()])
    submit = SubmitField("Submit")
