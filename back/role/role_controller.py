# from flask.views import MethodView
# from .role_repository import PlainRoleSchema, RoleModel, RoleRepository
# from flask_smorest import abort, Blueprint
# import jwt
# from flask import request, jsonify, g
# from marshmallow import ValidationError
# from ..location import PlainLocationSchema
#
# blp = Blueprint("roles", __name__, description="Operations on roles")
#
# @blp.route("/role")
# class Role(MethodView):
#     @blp.arguments(PlainRoleSchema)
#     @blp.response(200, PlainRoleSchema)
#     def post(self, organization_data):
#         role = RoleRepository.create(organization_data)
#         return role
#
#     @blp.response(200, PlainRoleSchema(many=True))
#     def get(self):
#         return RoleRepository.get_all_roles()
#
#
# @blp.route("/role/<integer:role_id>")
# class RoleGUD(MethodView):
#     @blp.response(200, PlainRoleSchema)
#     def get(self, role_id):
#         role = RoleRepository.get_role(role_id)
#         return role
#
#     def delete(self, role_id):
#         RoleRepository.delete_role(role_id)
#         return {'message': 'Role deleted successfully'}
#
#     @blp.arguments(PlainRoleSchema)
#     @blp.response(200, PlainRoleSchema)
#     def put(self, role_data, role_id):
#         role = RoleRepository.update_role(role_data, role_id)
#         return role
#
#
# @blp.errorhandler(ValidationError)
# def handle_validation_error(error):
#     print('Validation error:', error.messages)
#
#     response = jsonify({
#         'message': 'Validation error',
#         'errors': error.messages
#     })
#     response.status_code = 422
#     return response
#
# @blp.errorhandler(Exception)
# def handle_exception(error):
#     print('An error occurred:', str(error))
#
#     response = jsonify({
#         'message': 'An error occurred',
#         'error': str(error)
#     })
#     response.status_code = 500
#     return response