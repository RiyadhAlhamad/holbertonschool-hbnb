from flask_restx import Namespace, Resource, fields
from app.services import facade
import uuid
api = Namespace('places', description='Place operations')

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

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
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
                "amenities": [{'id': amenity.id, 'name': amenity.name} for amenity in place_new.amenities]
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
                ],
                "reviews": [
                    {
                        "id": r.id,
                        "text": r.text,
                        "rating": r.rating,
                        "user_id": r.user.id
                    } for r in p.reviews
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
                        ],
                        "reviews": [
                            {
                                "id": r.id,
                                "text": r.text,
                                "rating": r.rating,
                                "user_id": r.user.id
                            } for r in place.reviews
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
                        ],
                "reviews": [
                    {
                        "id": r.id,
                        "text": r.text,
                        "rating": r.rating,
                        "user_id": r.user.id
                    } for r in updated_place.reviews
                ]
                        }, 200
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_reviews_by_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': review.id, 'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                } for review in reviews], 200
    