from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email, Length, EqualTo

from undyingkingdoms.models.exports import User


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='You must enter a username.')])
    email = StringField('Email Address', validators=[Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password',
                             [DataRequired(message='You must enter a password.'),
                              Length(min=4),
                              EqualTo('confirmation', message='Passwords must match.')])
    confirmation = PasswordField('Repeat password')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.account_exists():
            return False
        return True

    def account_exists(self):
        if User.query.filter_by(email=self.email.data).first() is not None:
            self.email.errors.append("That email/account is already exists.")
            return True
