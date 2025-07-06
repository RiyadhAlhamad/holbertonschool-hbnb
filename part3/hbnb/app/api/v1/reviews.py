from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})



@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user['id']
        review_data['place_id'] = review_data.get('place_id')
        try:
            review_new = facade.create_review(review_data)
            return {
                "id": review_new.id,
                "text": review_new.text,
                "rating": review_new.rating,
                "place_id": review_new.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        review = facade.get_all_reviews()
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            }
            for r in review
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        is_admin = current_user.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized'}, 403

        review_data = api.payload
        try:
            update_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully',
                "text": update_review.text,
                "rating": update_review.rating,
                "user_id": update_review.user.id,
                "place_id": update_review.place.id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID"""
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        is_admin = current_user.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200