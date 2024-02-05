from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planets = db.relationship('Planets', lazy=True)
    favorite_people = db.relationship('People', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_people": [people.serialize() for people in self.favorite_people]
        }

    @property
    def favorite_planets_list(self):
        return [planet.serialize() for planet in self.favorite_planets]

    @property
    def favorite_people_list(self):
        return [people.serialize() for people in self.favorite_people]
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)
    home_planet = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    


    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "home_planet": self.home_planet,

        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    type_of_terrain = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    


    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type_of_terrain": self.type_of_terrain,
            "population": self.population,
            "diameter": self.diameter,
            "climate": self.climate,

        }
    
class People_favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relatioship = db.relationship(User)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    people_relatioship = db.relationship(People)

    def __repr__(self):
        return "{}".format(self.id)

    def serialize(self):
        return {
            "id" :self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }
    
class Planet_favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relatioship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    planet_relationship = db.relationship(Planets)

    def __repr__(self):
        return "{}".format(self.id)

    def serialize(self):
        return {
            "id" :self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }