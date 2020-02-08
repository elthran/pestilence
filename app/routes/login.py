from datetime import datetime
from random import randint

from flask import url_for, redirect, render_template, flash, jsonify
from flask.views import MethodView
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models.exports import Notification
from undyingkingdoms.models.forms.login import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/login.html')
def login(template):
    form = LoginForm()
    if current_user.is_authenticated:
        if not current_user.is_verified:
            return redirect(url_for('activate'))
        return redirect(url_for('overview'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.county is None:
                login_user(user)
                return redirect(url_for('initialize'))
            if user.get_last_logout() and user.county.day > 0 and (
                    datetime.utcnow() - user.get_last_logout()).total_seconds() // 3600 > 6:
                gold_reward = min((datetime.utcnow() - user.get_last_logout()).seconds // 3600, 48) * randint(5, 7)
                user.county.gold += gold_reward
                notification = Notification(
                    user.county,
                    "Login Reward",
                    f"Your people appreciate your trust in letting them run their own affairs. "
                    f"They give you {gold_reward} gold as a thank you.",
                )
                notification.save()
            login_user(user)
            if not user.is_verified:
                return redirect(url_for('activate'))
            return redirect(
                url_for('overview'))
        else:
            flash("Your email or password was incorrect.")
    return render_template(template, form=form)


class LoginAPI(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('overview'))
        form = LoginForm()
        return render_template("index/login.html", form=form)

    def post(self):
        form = LoginForm()
        if current_user.is_authenticated:
            return jsonify(
                status='success',
                message='User is already logged in. Redirect to overview page.',
                redirect=url_for('overview')
            ), 200
        elif form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                if current_user.county is None:
                    return jsonify(
                        status='success',
                        message='User is authenticated. Account has been reset. Redirect to initialize page.',
                        redirect=url_for('initialize')
                    ), 200
                else:
                    return jsonify(
                        status='success',
                        message='User has been logged in. Redirect to overview page.',
                        redirect=url_for('overview')
                    ), 200
            elif user:
                return jsonify(
                    status='fail',
                    message='Your email or password was incorrect.'
                ), 200
            else:
                return jsonify(
                    status='fail',
                    message='The requested user does not exist.'
                ), 200
        else:
            return jsonify(
                status='fail',
                message='The data sent is not in an acceptable form.',
                errors=form.errors
            ), 200

# app.add_url_rule('/login', view_func=LoginAPI.as_view('login_api'))
