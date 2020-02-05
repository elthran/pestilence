from flask_login import AnonymousUserMixin, UserMixin

from .templates import db, ModelState
from werkzeug.security import generate_password_hash, check_password_hash

from .worlds import World


class User(UserMixin, ModelState):
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(192), nullable=False)

    worlds = db.relationship('World', backref='user')
    highscores = db.relationship('Highscore', backref='user')

    # Flask
    is_authenticated = db.Column(db.Boolean)  # User has logged in through flask. (Flask)
    is_active = db.Column(db.Boolean)  # Account has been activated via email and not been locked. (Flask)
    is_anonymous = db.Column(db.Boolean)  # Current_user is set to is_anonymous when not yet logged in. (Flask)

    def __init__(self, username, password='123'):
        self.username = username
        self.set_password_hash(password)

        # Flask login
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute. Only password_hash is stored.')

    @property
    def world(self):
        world = World.query.filter(User.id == self.id).filter(World.active == True).first()
        return world

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<'User' {self.username}. ID {self.id}.>"


# class AnonymousUser(AnonymousUserMixin):
#     id = None
