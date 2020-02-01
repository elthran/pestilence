from .templates import db, ModelState


class World(ModelState):
    name = db.Column(db.String(64))
    cities = db.relationship('City', backref='world')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<'World' {self.name}. ID {self.id}. Belonging to User {self.user.username}>"

