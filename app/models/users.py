from .templates import db, ModelState


class User(ModelState):
    username = db.Column(db.String(64))

    def __init__(self, username):
        self.username = username
