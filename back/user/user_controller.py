from flask_smorest import abort, Blueprint
from flask.views import MethodView
from .user_repository import UserRepository, PlainUserSchema
import jwt
from flask import request, jsonify


blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)

    def post(self, user_data):
        user = UserRepository.register(user_data)
        return user

@blp.before_request
def check_authorization():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split('Bearer ')[1]
            decoded_token = jwt.decode(token, 'YOUR_SECRET_KEY', algorithms=['HS256'])
            request.decoded_token = decoded_token

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    else:
        return jsonify({'message': 'Missing Authorization header'}), 401

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserService.show(user_id)
        return user

    def delete(self, user_id):
        user = UserService.delete(user_id)
        return user


@blp.route("/user")
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserService.show_all()
