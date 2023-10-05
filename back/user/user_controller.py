from flask_smorest import abort, Blueprint
from flask.views import MethodView
from .user_repository import UserRepository, PlainUserSchema
from flask_jwt_extended import jwt_required, get_jwt
from flask import request, jsonify

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserRepository.register(user_data)
        return user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user_logged = UserRepository.user_login(user_data)
        return user_logged

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        user_logged_out = UserRepository.logout()
        return user_logged_out


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        new_token = UserRepository.refresh_token()
        return new_token
# @blp.before_request
# def check_authorization():
#     auth_header = request.headers.get('Authorization')
#     if auth_header:
#         try:
#             token = auth_header.split('Bearer ')[1]
#             decoded_token = jwt.decode(token, 'YOUR_SECRET_KEY', algorithms=['HS256'])
#             request.decoded_token = decoded_token
#
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Invalid token'}), 401
#     else:
#         return jsonify({'message': 'Missing Authorization header'}), 401

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, PlainUserSchema)
    def get(self, user_id):
        user = UserRepository.get_user(user_id)
        return user

    def delete(self, user_id):
        user = UserRepository.delete_user(user_id)
        return user


@blp.route("/user")
class UsersList(MethodView):
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        return UserRepository.show_all_users()

