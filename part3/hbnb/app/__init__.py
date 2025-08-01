from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
import config

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API',authorizations=authorizations,
            security='Bearer')
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'some‑strong‑secret'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)   
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    with app.app_context():
        db.create_all()
    return app
