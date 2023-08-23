from ..common_imports import *
from flask.views import MethodView
from flask_smorest import abort, Blueprint
import jwt
from flask import request, jsonify, g
from marshmallow import ValidationError
from ..utils import create_model

blp = Blueprint("intents", __name__, description="Operations on intents")

class IntentModel(db.Model):
    __tablename__ = "intents"
    id = db.Column(db.Integer, primary_key=True)
    intent = db.Column(db.String, unique=True)
    patterns = db.relationship("PatternModel", back_populates="intent")
    responses = db.relationship("ResponseModel", back_populates="intent")

class IntentSchema(Schema):
    id = fields.Str(dump_only=True)
    intent = fields.Str(required=True)

@blp.route("/intents")
class Intent(MethodView):
    @blp.arguments(IntentSchema)
    @blp.response(200, IntentSchema)
    def post(self, intent_data):
        intent = create_model(IntentModel, intent_data)
        return intent

