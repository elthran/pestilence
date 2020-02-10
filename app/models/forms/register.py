from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Length, EqualTo

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='You must enter a username.')])
    password = PasswordField('Password',
                             [DataRequired(message='You must enter a password.'),
                              Length(min=4)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.account_exists():
            return False
        return True

    def account_exists(self):
        if User.query.filter_by(username=self.username.data).first() is not None:
            self.username.errors.append("That username already exists.")
            return True
