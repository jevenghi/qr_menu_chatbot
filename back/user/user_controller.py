from flask_smorest import abort, Blueprint
from flask.views import MethodView
from .user_repository import UserRepository, PlainUserSchema, ChangePasswordSchema
from flask_jwt_extended import jwt_required, get_jwt

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
        user_logged = UserRepository.login(user_data)
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


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @jwt_required()
    @blp.response(200, PlainUserSchema)
    def get(self, user_id):
        user = UserRepository.get_user(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserRepository.delete_user(user_id)
        return user


@blp.route("/user/<int:user_id>/password")
class User(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(ChangePasswordSchema)
    def post(self, user_data, user_id):
        new_password = UserRepository.change_password(user_data, user_id)
        return new_password


@blp.route("/user")
class UsersList(MethodView):
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        return UserRepository.show_all_users()
