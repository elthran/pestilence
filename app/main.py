import uuid

from flask import render_template

from .config.initialize import initialize
from .models.users import User

app = initialize(__name__)


@app.route('/')
def root():
    """
    """
    user = User(uuid.uuid4())
    print(f"Created user {user.username} with id {user.id}")
    user.save()
    users = User.query.all()
    print("Here is a list of all users...")
    for user in users:
        print(f"User: {user.username} with id {user.id}")
    return str(users)
    # return render_template("layout.html", users=users)
