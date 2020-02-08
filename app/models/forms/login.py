from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[DataRequired(message='Must provide a password.')])
