from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.extensions import db, bcrypt ,jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'some‑strong‑secret'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  

    #instantiate Bcrypt.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)   #init db
    
    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
