from flask_restx import Namespace, Resource, fields
from app.services import facade

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
        """Register a new place"""
        place_data = api.payload
        existing_place = facade.get_place_by_title(place_data['title'])
        if existing_place:
            return {'message': 'Place with this title already exists'}, 400
        new_place = facade.create_place(place_data)
        return {'message': 'Place created successfully', 'place_id': new_place.id,'title': new_place.title,'description': new_place.description, 'price':new_place.price, 'latitude':new_place.latitude, 'longitude':new_place.longitude,'owner_id':new_place.owner, 'amenities':new_place.ameities }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places(), 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        return {'id': place.id,'title': place.title,'description': place.description,'price': place.price,'latitude': place.latitude,'longitude': place.longitude,'owner_id': place.owner ,'amenities': [amenity.id for amenity in place.amenities]}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        updated_place = facade.put_place(place_id, place_data)
        if not updated_place:
            return {'message': 'Place not found'}, 404
        return {'message': 'Place updated successfully', 'place_id': updated_place.id, 'title': updated_place.title, 'description': updated_place.description, 'price': updated_place.price, 'latitude': updated_place.latitude, 'longitude': updated_place.longitude, 'owner_id': updated_place.owner, 'amenities': [amenity.id for amenity in updated_place.amenities]}, 200