from flask import render_template, session
from flask_login import current_user, login_user

from .config.initialize import initialize
from .models import User, World, City

app = initialize(__name__, models=[World, User, City])


@app.route('/')
def root():
    """
    """
    print(session)
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
        city = City("Tokyo", world.id)
        city.save()

    world = World.query.first()
    print("User worlds,....:", user.worlds)
    print("My Worlds:", world)
    print("My Cities:", world.cities)
    print("Current user:", user)
    print("Flask user:", current_user)
    print("Flask session:", session)
    cities = world.cities # world.cities
    return render_template("home.html", users=[user], world=world, cities=cities)


# if session.new:
#     user = User("session new")
#     user.save()
    # session['anonymous_user_id'] = user.id
# else:
#     user = User.query.get(session['anonymous_user_id'])