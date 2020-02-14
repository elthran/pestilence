from numpy import unicode

from .templates import db, ModelState
from .sessions import Session
from werkzeug.security import generate_password_hash, check_password_hash

from .worlds import World


class User(ModelState):
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(192), nullable=False)

    worlds = db.relationship('World', backref='user')
    highscores = db.relationship('Highscore', backref='user')

    # Flask
    is_authenticated = db.Column(db.Boolean)  # User has logged in through flask. (Flask)
    is_active = db.Column(db.Boolean)  # Account has been activated via email and not been locked. (Flask)
    is_anonymous = db.Column(db.Boolean)  # Current_user is set to is_anonymous when not yet logged in. (Flask)

    # Sessions
    current_session_id = db.Column(db.Integer)

    # Lifetime values
    games_played = db.Column(db.Integer)

    def __init__(self, username):
        self.username = username
        self.password_hash = 'guest'

        # Flask login
        self.is_authenticated = True
        self.is_active = False
        self.is_anonymous = False

        # Lifetime values
        self.games_played = 0

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute. Only password_hash is stored.')

    @property
    def world(self):
        world = World.query.filter(User.id == self.id).filter(World.active == True).first()
        return world

    @property
    def session(self):
        if self.current_session_id:
            session = Session.query.get(self.current_session_id)
        else:
            self.start_session()
            session = self.session
        return session

    @property
    def time_played_in_seconds(self):
        sessions = Session.query.filter(Session.user_id == self.id).all()
        return sum(session.length_in_seconds for session in sessions)

    def get_id(self):
        """Used by Flask to get the User ID to be used in a session. Must be unique.
        If the user wants to change passwords and log out of all devices, this value needs to change."""
        return unicode(str(self.id) + self.password_hash)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def start_session(self):
        if self.current_session_id:
            self.end_session()
        session = Session(self.id)
        session.save()
        self.current_session_id = session.id

    def end_session(self):
        session = Session.query.get(self.current_session_id)
        session.session_heartbeat()
        self.current_session_id = None

    def __repr__(self):
        return f"<'User' {self.username}. ID {self.id}.>"
