from .templates import db, ModelState


class City(ModelState):
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(64))
    population = db.Column(db.Integer)
    sick = db.Column(db.Integer)
    deaths = db.Column(db.Integer)

    def __init__(self, name, world_id):
        self.name = name
        self.world_id = world_id

    def __repr__(self):
        return f"<'City' {self.name}. ID {self.id}. Belonging to User {self.world.user.username}>"
