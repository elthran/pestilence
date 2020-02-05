from .templates import db, ModelState


class Highscore(ModelState):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    world_id = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, user_id, world_id, score):
        self.user_id = user_id
        self.world_id = world_id
        self.score = score

    def __repr__(self):
        return f"<'Highscore' with ID {self.id}.>"

