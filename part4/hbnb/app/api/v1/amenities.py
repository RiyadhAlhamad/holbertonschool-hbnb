from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin creates a new amenity"""
        current_user = get_jwt_identity()

        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve the list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name
            }
            for a in amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
            }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Admin updates amenity"""
        current_user = get_jwt_identity()

        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload
        update_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not update_amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': update_amenity.id,
            'name': update_amenity.name
        }, 200


