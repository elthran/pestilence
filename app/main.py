import uuid

from flask import render_template

from .config.initialize import initialize
from .models import User, World, City

app = initialize(__name__, models=[World, User, City])


@app.route('/')
def root():
    """
    """
    users = User.query.all()
    world = World.query.first()
    cities = City.query.all()
    return render_template("home.html", users=users, world=world, cities=cities)
