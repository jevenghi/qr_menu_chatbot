from marshmallow import Schema, fields
from ..db import db
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, create_refresh_token, get_jwt_identity
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from datetime import timezone

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class TokenBlocklist(db.Model):
    __tablename__ = "tokens_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(required=True, load_only=True)
    confirm_new_password = fields.Str(required=True, load_only=True)





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
    def user_login(user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

    @staticmethod
    def get_user(user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

    @staticmethod
    def show_all_users():
        return UserModel.query.all()


    @staticmethod
    def logout():
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))

        refresh_token_jti = get_jwt()["refresh_token"]["jti"]
        db.session.add(TokenBlocklist(jti=refresh_token_jti, created_at=now))

        db.session.commit()
        return {"message": "JWT revoked"}
    @staticmethod
    def refresh_token():
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

    @staticmethod
    def change_password(user_data, user_id):
        user = UserModel.query.get(user_id)
        if not pbkdf2_sha256.verify(user_data["old_password"], user.password):
            return {"message": "Wrong password"}
        if user_data["new_password"] != user_data["confirm_new_password"]:
            return {"message": "Passwords don't match"}
        user.password = pbkdf2_sha256.hash(user_data["new_password"])
        db.session.commit()
        return {"message": "Password changed"}