import math
import random

from .templates import db, ModelState


class City(ModelState):
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(64))
    population = db.Column(db.Integer)
    infected = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    dead = db.Column(db.Integer)

    def __init__(self, name, world_id, population=7000000):
        self.name = name
        self.world_id = world_id
        self.population = population
        self.infected = 0
        self.recovered = 0
        self.dead = 0

    @property
    def susceptible(self):
        """
        People are have a chance of catching the disease.
        """
        return self.population - self.infected - self.recovered

    def update_deaths(self, mortality):
        """
        Check if any infected people have died.
        """
        new_deaths = int(math.floor((self.infected * mortality / 100) + random.random()))
        self.population -= new_deaths
        self.dead += new_deaths

    def update_recovered(self, duration):
        """
        Let some infected people recover each day.
        """
        new_recoveries = int(math.floor(((20 - duration) / 100) + random.random()))
        self.recovered += new_recoveries

    def update_infected(self, infectiousness):
        """
        If there are susceptible people and infected people in the same city, see how many more become infected.
        """
        if 0 < self.infected < 50:  # if only a few are infected, make it random.
            new_infected_infections = None
            new_infected_infections_rounded = random.randint(1, 10)
        else:  # Otherwise use a population growth model.
            new_infected_infections = (infectiousness / 100) * self.infected * ((self.susceptible - self.infected) / self.susceptible)
            new_infected_infections_rounded = int(math.floor(new_infected_infections + random.random()))
        self.infected += new_infected_infections_rounded

    def update_population(self, disease):
        if self.infected > 0 and disease is None:
            raise ValueError("People are infected with an unknown disease.")
        elif self.infected > 0 and disease:
            self.update_deaths(disease.mortality)
            self.update_recovered(disease.duration)
            self.update_infected(disease.infectiousness)
        elif self.infected == 0 and disease is None:
            pass
        elif self.infected == 0 and disease:
            self.infected = 1

    def __repr__(self):
        return f"<'City' {self.name}. ID {self.id}. Belonging to User {self.world.user.username}>"
