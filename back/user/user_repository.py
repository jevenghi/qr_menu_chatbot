from marshmallow import Schema, fields
from db import db
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    roles = db.relationship('RoleModel', secondary='user_roles')


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRepository:
    @staticmethod
    def register(user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="This e-mail is already registered.")

        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201

    @staticmethod
    def show(user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @staticmethod
    def delete(user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

    @staticmethod
    def show_all():
        return UserModel.query.all()