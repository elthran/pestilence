from .templates import db, ModelState


class World(ModelState):
    cities = db.relationship('City', backref='world')
    name = db.Column(db.String(64))

    def __init__(self, name="Default"):
        self.name = name
