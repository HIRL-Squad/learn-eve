from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    submit = SubmitField("Log In")

    username = StringField('Username', validators=[
        DataRequired('Please provide a username'),
        Length(min=3, message=(u'Username too short'))])
    password = PasswordField('Pick a secure password', validators=[
        DataRequired(),
        Length(min=6, message=(u'Please give a longer password'))])
