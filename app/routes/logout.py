from flask import redirect, url_for
from flask_login import logout_user, current_user


@app.route('/logout/')
def logout():
    current_user.end_session()
    logout_user()
    return redirect(url_for('home'))
