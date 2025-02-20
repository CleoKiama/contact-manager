from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    mobile = StringField(
        "Mobile Phone Number", validators=[DataRequired(), Length(min=10, max=15)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[DataRequired()])
    registration_number = StringField(
        "Registration Number", validators=[DataRequired()]
    )
    submit = SubmitField("Add Contact")
