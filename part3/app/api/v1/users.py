from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.models.user import User
from app.services.facade import facade

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@ns.route('/')
class UserList(Resource):

    def get(self):
        return [u.to_dict() for u in facade.list_users()]

    @ns.expect(user_model)
    def post(self):

        data = request.json

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        try:

            user = User(
                data['first_name'],
                data['last_name'],
                data['email'],
                data['password'],
                data.get('is_admin', False)
            )

            facade.create_user(user)

            return user.to_dict(), 201

        except ValueError as e:

            return {'error': str(e)}, 400


@ns.route('/<string:user_id>')
class UserResource(Resource):

    def get(self, user_id):

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict()

    @jwt_required()
    @ns.expect(user_model)
    def put(self, user_id):

        current_user_id = get_jwt_identity()

        claims = get_jwt()

        is_admin = claims.get('is_admin')

        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized'}, 403

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        data = request.json

        if not is_admin:

            if 'email' in data or 'password' in data:
                return {
                    'error': 'Regular users cannot modify email or password'
                }, 403

        if is_admin:

            if 'email' in data:

                duplicate = facade.get_user_by_email(data['email'])

                if duplicate and duplicate.id != user_id:
                    return {'error': 'Email already in use'}, 400

                user.email = data['email']

            if 'password' in data:

                from app import bcrypt

                user.password = bcrypt.generate_password_hash(
                    data['password']
                ).decode('utf-8')

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        user.update()

        return user.to_dict(), 200