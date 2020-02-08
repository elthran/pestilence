from flask import redirect, url_for
from flask_login import logout_user, current_user

from undyingkingdoms import app


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    current_user.in_active_session = False
    logout_user()
    return redirect(url_for('home'))
