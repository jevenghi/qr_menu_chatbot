from flask.views import MethodView
from .role_repository import PlainRoleSchema, RoleModel, RoleRepository
from flask_smorest import abort, Blueprint
import jwt
from flask import request, jsonify, g
from marshmallow import ValidationError
from ..location import PlainLocationSchema

blp = Blueprint("roles", __name__, description="Operations on roles")

@blp.route("/role")
class Role(MethodView):
    @blp.arguments(PlainRoleSchema)
    @blp.response(200, PlainRoleSchema)
    def post(self, organization_data):
        role = RoleRepository.create(organization_data)
        return role

    @blp.response(200, PlainRoleSchema(many=True))
    def get(self):
        return RoleRepository.get_all_roles()


@blp.route("/organization/<string:organization_id>")
class OrganizationGUD(MethodView):
    @blp.response(200, PlainLocationSchema(many=True))
    def get(self, organization_id):
        organization_locations = OrganizationRepository.get_locations(organization_id)
        return organization_locations


    def delete(self, organization_id):
        OrganizationRepository.delete_organization(organization_id)
        return {'message': 'Organization deleted successfully'}

    @blp.arguments(PlainOrganizationSchema)
    @blp.response(200, PlainOrganizationSchema)
    def put(self, organization_data, organization_id):
        organization = OrganizationRepository.update_organization(organization_data, organization_id)
        return organization


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