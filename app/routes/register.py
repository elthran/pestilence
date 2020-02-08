from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template
from undyingkingdoms import app, User
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/register.html')
def register(template):
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview'))

    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        user.save()
        login_user(user)
        return redirect(url_for('initialize'))
    return render_template(template, form=form)
