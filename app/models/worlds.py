import random

from .templates import db, ModelState
from .tickers import Ticker


class World(ModelState):
    name = db.Column(db.String(64))
    day = db.Column(db.Integer)
    cities = db.relationship('City', backref='world')
    diseases = db.relationship('Disease', backref='world')
    tickers = db.relationship('Ticker', backref='world')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.day = 0

    def pass_time(self):
        self.day += 1
        if self.day > 2:
            newly_infected = random.randint(0, self.day * 2)
            self.diseases[0].infected += newly_infected
            newly_dead = random.randint(0, (self.diseases[0].infected - self.diseases[0].deaths) // 4)
            self.diseases[0].deaths += random.randint(0, newly_dead)
        self.update_ticker()

    def update_ticker(self):
        ticker = None
        city = random.choice(self.cities).name
        if self.day == 1:
            ticker = Ticker(self.day,
                            f"A new disease called {self.diseases[0].name} was reported.",
                            self.id)
        elif self.day % 7 == 4:
            ticker = Ticker(self.day,
                            f"The disease has broken out in {city}.",
                            self.id)
        if self.day == 9:
            ticker = Ticker(self.day,
                            f"The city of {city} has begun working on a cure for {self.diseases[0].name}.",
                            self.id)
        if ticker:
            ticker.save()

    def __repr__(self):
        return f"<'World' {self.name}. ID {self.id}. Belonging to User {self.user.username}>"

