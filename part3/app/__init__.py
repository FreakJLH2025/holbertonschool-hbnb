import os
from flask import Flask, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_PATH = os.path.join(BASE_DIR, 'part4', 'base_files')

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: Bearer <your_token>'
    }
}

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    @app.route('/')
    @app.route('/index.html')
    def serve_index():
        return send_from_directory(FRONTEND_PATH, 'index.html')

    @app.route('/login.html')
    def serve_login():
        return send_from_directory(FRONTEND_PATH, 'login.html')

    @app.route('/place.html')
    def serve_place():
        return send_from_directory(FRONTEND_PATH, 'place.html')

    @app.route('/add_review.html')
    def serve_add_review():
        return send_from_directory(FRONTEND_PATH, 'add_review.html')

    @app.route('/add_place.html')
    def serve_add_place():
        return send_from_directory(FRONTEND_PATH, 'add_place.html')

    @app.route('/register.html')
    def serve_register():
        return send_from_directory(FRONTEND_PATH, 'register.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(FRONTEND_PATH, path)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB REST API',
        authorizations=authorizations,
        security='Bearer',
        doc='/docs'
    )

    from app.api.v1.users import ns as users_ns
    from app.api.v1.amenities import ns as amenities_ns
    from app.api.v1.places import ns as places_ns
    from app.api.v1.reviews import ns as reviews_ns
    from app.api.v1.auth import ns as auth_ns

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
