from .templates import db, ModelState


class Disease(ModelState):
    name = db.Column(db.String(64))
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    type = db.Column(db.String(64)) # Bacteria, viruses, fungi, protozoa, parasites, and prions
    points = db.Column(db.Integer)
    mortality = db.Column(db.Integer)  # Affects number who die after infected
    infectiousness = db.Column(db.Integer)  # Affects rate of spread
    duration = db.Column(db.Integer)  # How many days on average someone will suffer from the disease
    resistance = db.Column(db.Integer)  # Delays rate at which a cure can be found

    def __init__(self, name, world_id):
        self.name = name
        self.world_id = world_id
        self.type = None
        self.points = 5
        self.mortality = 1  # Starts at 1%
        self.infectiousness = 1  # Starts at 1%
        self.duration = 3  # Starts at 3 days
        self.resistance = 0  # Starts at 0%

    @property
    def infected(self):
        infected = 0
        for city in self.world.cities:
            infected += city.infected
        return infected

    @property
    def dead(self):
        dead = 0
        for city in self.world.cities:
            dead += city.dead
        return dead

    def assign_type(self, type):
        if type in ("bacterium", "virus") and self.type is None:
            self.type = type
            if type == "bacterium":
                self.points -= 3
                self.mortality += 3
            if type == "virus":
                self.points -= 2
                self.resistance += 2
        else:
            pass

    def upgrade_trait(self, trait):
        if trait in ("mortality", "infectiousness", "resistance") and self.points > 0:
            setattr(self, trait, getattr(self, trait) + 1)
            self.points -= 1
        else:
            pass

    def __repr__(self):
        return f"<'Disease' {self.name}. ID {self.id}. Belonging to User {self.world.user.username}>"

