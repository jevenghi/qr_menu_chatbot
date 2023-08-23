from flask.views import MethodView
from .organization_repository import OrganizationRepository, PlainOrganizationSchema, OrganizationModel
from flask_smorest import abort, Blueprint
import jwt
from flask import request, jsonify, g
from marshmallow import ValidationError

blp = Blueprint("organizations", __name__, description="Operations on organizations")

@blp.route("/organization")
class Organization(MethodView):
    @blp.arguments(PlainOrganizationSchema)
    @blp.response(200, PlainOrganizationSchema)
    def post(self, organization_data):
        organization = OrganizationRepository.create(organization_data)
        return organization

    @blp.response(200, PlainOrganizationSchema(many=True))
    def get(self):
        return OrganizationModel.query.all()




@blp.errorhandler(ValidationError)
def handle_validation_error(error):
    print('Validation error:', error.messages)

    response = jsonify({
        'message': 'Validation error',
        'errors': error.messages
    })
    response.status_code = 422
    return response

@blp.errorhandler(Exception)
def handle_exception(error):
    print('An error occurred:', str(error))

    response = jsonify({
        'message': 'An error occurred',
        'error': str(error)
    })
    response.status_code = 500
    return response