from flask import render_template, session, url_for
from flask_login import current_user, login_user
from werkzeug.utils import redirect

from .config.initialize import initialize
from .models import User, World, City, Disease, Ticker

app = initialize(__name__, models=[World, User, City])


@app.route('/')
def root():
    """
    """
    if current_user.is_authenticated:
        # If the player has logged in through Flask, use that account.
        user = current_user
    else:
        # Otherwise, use a newly created Guest account.
        user = User("Guest")
        user.save()
        login_user(user)
    if user.worlds == []:
        world = World("Simple Earth", user.id)
        world.save()
        for name in ["Taipei", "Vancouver"]:
            city = City(name, world.id)
            city.save()
        disease = Disease("Poop-panda Disease", world.id)
        disease.save()
    world = user.worlds[0]
    cities = world.cities
    disease = world.diseases[0]
    world.pass_time()
    return render_template("home.html",
                           user=user,
                           world=world,
                           disease=disease,
                           tickers=world.tickers)


@app.route('/select_type/<string:type>')
def select_type(type):
    """
    """
    disease = current_user.worlds[0].diseases[0]
    disease.assign_type(type)
    return redirect(url_for('root'))


@app.route('/upgrade_trait/<string:trait>')
def upgrade_trait(trait):
    """
    """
    disease = current_user.worlds[0].diseases[0]
    disease.upgrade_trait(trait)
    return redirect(url_for('root'))


# if session.new:
#     user = User("session new")
#     user.save()
    # session['anonymous_user_id'] = user.id
# else:
#     user = User.query.get(session['anonymous_user_id'])