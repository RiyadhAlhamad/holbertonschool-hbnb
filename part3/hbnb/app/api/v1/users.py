from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @jwt_required()
    def post(self):
        """Admin creates a new user"""
        current_user = get_jwt_identity()

        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        user_data['password'] = User.hash_password(user_data['password'])

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'User successfully listed')
    def get(self):
        """Get all users"""
        all_users = facade.get_all_users()
        return [{'id': users.id, 'first_name': users.first_name, 'last_name': users.last_name, 'email': users.email} for users in all_users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)

        # إذا المستخدم مش أدمن، لازم يكون يعدل نفسه فقط
        if not is_admin and user_id != current_user["id"]:
            return {"error": "Unauthorized action"}, 403

        user_data = api.payload

        # المستخدم العادي ما يعدل ايميل أو باسورد
        if not is_admin and ("email" in user_data or "password" in user_data):
            return {"error": "You cannot modify email or password"}, 400

        # تأكد الإيميل غير مكرر
        if "email" in user_data:
            existing = facade.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                return {"error": "Email already in use"}, 400

        # هش للباسورد إذا موجود
        if "password" in user_data:
            user_data["password"] = User.hash_password(user_data["password"])

        updated_user = facade.put_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

