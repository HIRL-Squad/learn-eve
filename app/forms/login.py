from flask_babelex import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    submit = SubmitField(u'Log In')

    username = StringField(lazy_gettext(u'Username'), validators=[
        DataRequired(u'Please provide a username'),
        Length(min=3, message=lazy_gettext(u'Please provide a username'))])
    password = PasswordField(lazy_gettext('Pick a secure password'), validators=[
        DataRequired(),
        Length(min=6, message=lazy_gettext(u'Please give a longer password'))])
