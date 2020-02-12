from datetime import datetime

from .templates import db, ModelEvent


class Session(ModelEvent):
    user_id = db.Column(db.Integer)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    length = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id

    def end_session(self):
        self.logout_time = datetime.utcnow
        print(self.login_time, self.logout_time)
        self.length = (self.logout_time - self.login_time).seconds


