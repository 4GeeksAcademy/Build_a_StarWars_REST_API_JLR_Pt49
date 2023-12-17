"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Traer todos los usuarios
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = list(map(lambda user: user.serialize(), all_users))

    return jsonify(result), 200

#Traer un usuario por ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    one_user = User.query.filter_by(id=user_id).first()

    basic_info = request.args.get('basic', False)

    if basic_info and basic_info.lower() == 'true':
        return jsonify(one_user.serialize_basic()), 200
    else:
        return jsonify(one_user.serialize()), 200

#Traer los favoritos de un usuario
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorite(user_id):
    user = User.query.get(user_id)

    user_planets = user.favorite_planets
    serialized_planets = [planet.serialize() for planet in user_planets]

    user_people = user.favorite_people
    serialized_people = [people.serialize() for people in user_people]

    response_body = {
        "favorite_people": serialized_people,
        "favorite_planets": serialized_planets
    }

    return jsonify(response_body), 200

#Agregar un planeta favorito a un usuario
@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def post_user_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    user.favorite_planets.append(planet)
    db.session.commit()

    response_body = {"msg": f"El planeta {planet.name} se agregó correctamente al usuario!"}
    return jsonify(response_body), 200

#Agregar un personaje favorito a un usuario
@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def post_user_favorite_person(user_id, people_id):
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    user.favorite_people.append(people)
    db.session.commit()

    response_body = {"msg": f"El personaje {people.name} se agregó correctamente al usuario!"}
    return jsonify(response_body), 200

#Traer a todos los personajes
@app.route('/people', methods=['GET'])
def get_character():
    all_people = People.query.all()
    result = list(map(lambda character: character.serialize(), all_people))
    
    return jsonify(result), 200

#Traer un personaje por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    character = People.query.filter_by(id=people_id).first()

    return jsonify(character.serialize()), 200

#Traer todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    result = list(map(lambda place: place.serialize(), all_planets))
    
    return jsonify(result), 200

#Traer un planeta por ID
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    print(planets_id)
    planet = Planets.query.filter_by(id=planets_id).first()
    print(planet)

    return jsonify(planet.serialize()), 200


#Eliminar un personaje favorito de un usuario
@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_user_favorite_person(user_id, people_id):
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    user.favorite_people.remove(people)
    db.session.commit()

    response_body = {"msg": f"El personaje {people.name} se elimino correctamente del usuario!"}
    return jsonify(response_body), 200

#Eliminar un planeta favorito de un usuario
@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_user_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    user.favorite_planets.remove(planet)
    db.session.commit()

    response_body = {"msg": f"El planeta {planet.name} se elimino correctamente del usuario!"}
    return jsonify(response_body), 200

# Agregar un planeta nuevo desde la api
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()

    new_planet = Planets(
        name=data['name'],
        climate=data['climate'],
        type_of_terrain=data['type_of_terrain'],
        diameter=data['diameter'],
        population=data['population']
    )

    db.session.add(new_planet)
    db.session.commit()

    response_body = {"msg": f"El planeta {new_planet.name} se agregó correctamente."}
    return jsonify(response_body)

# Agregar un personaje nuevo desde la api
@app.route('/people', methods=['POST'])
def add_people():
    data = request.get_json()

    new_character = People(
        name=data['name'],
        eye_color=data['eye_color'],
        gender=data['gender'],
        height=data['height'],
        home_planet=data['home_planet']
    )

    db.session.add(new_character)
    db.session.commit()

    response_body = {"msg": f"El personaje {new_character.name} se agregó correctamente."}
    return jsonify(response_body)

# Editar un Planeta desde la api
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def edit_planet(planet_id):
    planet = Planets.query.get(planet_id)

    data = request.get_json()

    planet.name = data.get('name', planet.name)
    planet.climate = data.get('climate', planet.climate)
    planet.type_of_terrain = data.get('type_of_terrain', planet.type_of_terrain)
    planet.diameter = data.get('diameter', planet.diameter)
    planet.population = data.get('population', planet.population)
    

    db.session.commit()

    response_body = {"msg": f"El planeta {planet.name} se editó correctamente."}
    return jsonify(response_body)

# Editar un personaje desde la api
@app.route('/people/<int:people_id>', methods=['PUT'])
def edit_people(people_id):
    people = People.query.get(people_id)

    data = request.get_json()

    people.name = data.get('name', people.name)
    people.eye_color = data.get('eye_color', people.eye_color)
    people.gender = data.get('gender', people.gender)
    people.height = data.get('height', people.height)
    people.home_planet = data.get('home_planet', people.home_planet)
    

    db.session.commit()

    response_body = {"msg": f"El personaje {people.name} se editó correctamente."}
    return jsonify(response_body)

# Eliminar un planeta desde la Api
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    db.session.delete(planet)
    db.session.commit()

    response_body = {"msg": f"El planeta {planet.name} se eliminó correctamente."}
    return jsonify(response_body)

# Eliminar un personaje desde la api
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_character(people_id):
    people = People.query.get(people_id)

    db.session.delete(people)
    db.session.commit()

    response_body = {"msg": f"El personaje {people.name} se eliminó correctamente."}
    return jsonify(response_body)










# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
