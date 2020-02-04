import math
import random

from .templates import db, ModelState
from .tickers import Ticker
from .cities import City


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
        self.day = -1

    def pass_time(self):
        if self.day == 25:
            print(f"GAME OVER. YOUR SCORE WAS {self.diseases[0].dead}")
            return False

        infected_cities = [city for city in self.cities if city.infected > 0]
        uninfected_cities = [city for city in self.cities if city.infected == 0]

        if len(infected_cities) == 0:
            city = random.choice(uninfected_cities)
            city.update_population(self.diseases[0])
            self.update_ticker(city=city, reason="first")
        else:
            for city in infected_cities:
                city.update_population(self.diseases[0])

            for city in uninfected_cities:  # Check if the disease spreads to a new city
                if random.randint(1, 10) == 10:
                    city.update_population(self.diseases[0])
                    self.update_ticker(city=city, reason="new")

        self.update_ticker()
        self.day += 1

    def update_ticker(self, city=None, reason=None):
        if reason:
            ticker = None
            if reason == "first":
                ticker = Ticker(self.day,
                                f"The {self.diseases[0].name} has been discovered in {city.name}.",
                                self.id)
            elif reason == "new":
                ticker = Ticker(self.day,
                                f"The disease has reportedly spread to {city.name}.",
                                self.id)
            ticker.save()

    def __repr__(self):
        return f"<'World' {self.name}. ID {self.id}. Belonging to User {self.user.username}>"

