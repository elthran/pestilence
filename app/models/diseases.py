from .templates import db, ModelState


class Disease(ModelState):
    name = db.Column(db.String(64))
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    type = db.Column(db.String(64)) # Bacteria, viruses, fungi, protozoa, parasites, and prions
    points = db.Column(db.Integer)
    infected = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mortality = db.Column(db.Integer)
    infectiousness = db.Column(db.Integer)

    def __init__(self, name, world_id):
        self.name = name
        self.world_id = world_id
        self.type = None
        self.points = 5
        self.mortality = 1
        self.infectiousness = 1
        self.infected = 0
        self.deaths = 0

    def assign_type(self, type):
        if type in ("bacterium", "virus") and self.type is None:
            self.type = type
            if type == "bacterium":
                self.points -= 3
            if type == "virus":
                self.points -= 2
        else:
            pass

    def upgrade_trait(self, trait):
        if trait in ("mortality", "infectiousness") and self.points > 0:
            setattr(self, trait, getattr(self, trait) + 1)
            self.points -= 1
        else:
            pass

    def __repr__(self):
        return f"<'Disease' {self.name}. ID {self.id}. Belonging to User {self.world.user.username}>"

