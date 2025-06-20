from flask_restx import Namespace, Resource, fields
from app.services import facade
import uuid
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new place """
        place_data = api.payload
        try:
            place_new = facade.create_place(place_data)

            return {
                "Place id": place_new.id,
                "title": place_new.title,
                "description": place_new.description,
                "price": place_new.price,
                "latitude": place_new.latitude,
                "longitude": place_new.longitude,
                "owner_id": place_new.owner.id,
                "amenities": [amenity.id for amenity in place_new.amenities],
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                "Place id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [
                    {
                        "id": a.id,
                        "name": a.name
                    } for a in p.amenities
                ]
            }
            for p in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        return {
                "Place id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                        "owner": {
                            "id": place.owner.id,
                            "first_name": place.owner.first_name,
                            "last_name": place.owner.last_name,
                            "email": place.owner.email
                        },
                        "amenities": [
                            {
                                "id": a.id,
                                "name": a.name
                            } for a in place.amenities
                        ]            
                }, 200
                
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'message': 'Place not found'}, 404
        return {'message': 'Place updated successfully', 
                "Place id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner.id,
                "amenities": [
                    {
                        "id": a.id,
                        "name": a.name
                        } for a in updated_place.amenities
                        ]
                        }, 200