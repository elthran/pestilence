from datetime import datetime

from .templates import db, ModelEvent


class Session(ModelEvent):
    user_id = db.Column(db.Integer)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    length_in_seconds = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id

    def session_heartbeat(self):
        if (datetime.utcnow() - self.login_time).seconds > 600:
            # If the time between heartbeats is too long, maybe we want to start a new sesion.
            pass
        self.logout_time = datetime.utcnow()
        if self.logout_time <= self.login_time:
            self.length_in_seconds = 0
        elif self.logout_time > self.login_time:
            self.length_in_seconds = (self.logout_time - self.login_time).seconds

