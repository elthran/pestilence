from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='You must enter a username.')])
    password = PasswordField('Password', validators=[DataRequired(message='Must provide a password.')])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True
