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
from models import db, Usuarios, Planetas, Personajes, Favoritos
import datetime
#from models import Person


## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():

    # get all the favorites
    # map the results and your list of people  inside of the all_people variable
    query = Personajes.query.all()
    results = list(map(lambda personajes: personajes.serialize(), query))
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):

    # get all the favorites
    # map the results and your list of people  inside of the all_people variable
    query = Personajes.query.get(people_id)
    results = query.serialize()
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():

    # get all the favorites
    # map the results and your list of people  inside of the all_people variable
    query = Planetas.query.all()
    results = list(map(lambda planetas: planetas.serialize(), query))
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets(planetas_id):

    # get all the favorites
    # map the results and your list of people  inside of the all_people variable
    query = Planetas.query.get(planetas_id)
    results = query.serialize()
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_all_users():

    query = Usuarios.query.all()
    results = list(map(lambda usuarios: usuarios.serialize(), query))
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    query = Favoritos.query.filter_by(usuario_id=user_id)
    results = list(map(lambda favoritos: favoritos.serialize(), query))
    for result  in results:
        if result.get("planetas_id") == None:
            query_personajes = Personajes.query.get(result.get("personajes_id"))
            result ["nombre"] = query_personajes.serialize().get("nombre")
        else:
            query_planets = Planetas.query.get(result.get("planetas_id"))
            result ["nombre"] = query_planetas.serialize().get("nombre")
    response_body = {
        "message": results
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['POST'])
@jwt_required()
def add_favorites():
    user_id = get_jwt_identity()
    request_favoritos=request.get_json() 
    usuario_favoritos = Favoritos(usuario_id = user_id, planetas_id = request_favoritos["planetas_id"], personajes_id = request_favoritos["personajes_id"])
    print(usuario_favoritos)
    db.session.add(usuario_favoritos)
    db.session.commit()
    response_body = {
        "message": "added"
    }
    return jsonify(response_body),200

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def delete_favorites(favorite_id):
    user_id = get_jwt_identity()
    fav_delete=Favoritos.query.get(favorite_id)
    if fav_delete is None:
        raise APIException('Favoritos not found', status_code=404)
    print(user_id)
    if fav_delete.serialize().get("usuario_id") != user_id:
        raise APIException('No autorizado', status_code=404)
    db.session.delete(fav_delete)
    db.session.commit()
    response_body = {
        "message": "removed"
    }
    return jsonify(response_body), 200

@app.route('/register', methods=["POST"])
def registro():
    if request.method == 'POST':
        usuario = request.json.get("usuario", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        apellido_1 = request.json.get("apellido_1", None)
        apellido_2 = request.json.get("apellido_2", None)

        if not usuario:
            return jsonify({"message": " Se necesita usuario"}), 400

        if not email:
            return jsonify({"message": " Se necesita un email"}), 400

        if not password:
            return jsonify({"message": "Se necesita una contraseña"}), 400

        if not apellido_1:
            return jsonify({"message": "Se necesita el apellido 1"}), 400

        if not apellido_2:
            return jsonify({"message": "Se necesita el apellido 2"}), 400

        user = Usuarios.query.filter_by(email=email).first()
        print(user)
        if user:
            return jsonify({"message": "Este usuario ya existe"}), 400

        user = Usuarios()
        user.email = email
        user.usuario = usuario
        user.apellido_1 = apellido_1
        user.apellido_2 = apellido_2
        hashed_password = generate_password_hash(password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"ok": "Se registro con exito!", "status": "true"}), 200

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"message": "Nombre de usuario requerido"}), 400

        if not password:
            return jsonify({"message": "Contraseña requerida"}), 400

        user = Usuarios.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "El nombre de usuario es incorrecto"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"message": "La contraseña es incorrecta"}), 401

        expiracion = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.id, expires_delta=expiracion)

        print("test")
        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

