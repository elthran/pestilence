from flask import render_template, session, url_for
from flask_login import current_user, login_user
from sqlalchemy import func
from werkzeug.utils import redirect

from .config.initialize import initialize
from .models import User, World, City, Disease, Ticker, Highscore

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
    # Get the most recent World of the user? Maybe each world has an ACTIVE boolean instead?
    world = user.world
    if world:
        disease = world.diseases[0]
        world.pass_time()
        print("first:", world.id)
    else:
        disease = None
    print("all:", user.worlds)
    highscores = Highscore.query.all()
    print(highscores)
    return render_template("home.html",
                           user=user,
                           world=world,
                           disease=disease,
                           highscores=highscores)


@app.route('/select_type/<string:type>')
def select_type(type):
    """
    """
    disease = current_user.world.diseases[0]
    disease.assign_type(type)
    return redirect(url_for('root'))


@app.route('/upgrade_trait/<string:trait>')
def upgrade_trait(trait):
    """
    """
    disease = current_user.world.diseases[0]
    disease.upgrade_trait(trait)
    return redirect(url_for('root'))


@app.route('/start_game/')
def start_game():
    """
    """
    user = current_user
    world = World.query.filter(User.id == user.id).filter(World.active == True).first()
    if world:
        # This user already has an active game
        return redirect(url_for('root'))
    world = World("Simple Earth", user.id)
    world.save()
    for name in ["Taipei", "Vancouver"]:
        city = City(name, world.id)
        city.save()
    disease = Disease("Poop-panda Disease", world.id)
    disease.save()
    return redirect(url_for('root'))


# if session.new:
#     user = User("session new")
#     user.save()
    # session['anonymous_user_id'] = user.id
# else:
#     user = User.query.get(session['anonymous_user_id'])