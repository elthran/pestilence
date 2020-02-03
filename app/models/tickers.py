from .templates import db, ModelState


class Ticker(ModelState):
    day = db.Column(db.Integer)
    message = db.Column(db.String(128))
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)

    def __init__(self, day, message, world_id):
        self.day = day
        self.message = message
        self.world_id = world_id

    def __repr__(self):
        return f"<'Ticker' with ID {self.id}. Belonging to User {self.world.user.username}>"

