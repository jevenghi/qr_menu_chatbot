# from ..common_imports import *
# from ..location import PlainLocationSchema, LocationModel
# from ..db import db
# from ..utils import create_model
#
# class RoleModel(db.Model):
#     __tablename__ = "roles"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#
# class PlainRoleSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)
#
# class RoleRepository:
#     @staticmethod
#     def create(data):
#         return create_model(RoleModel, data)
#
#     @staticmethod
#     def get_role(role_id):
#         role = RoleModel.query.get_or_404(role_id)
#         return role
#
#     @staticmethod
#     def delete_role(role_id):
#         role = RoleModel.query.get(role_id)
#         db.session.delete(role)
#         db.commit()
#     @staticmethod
#     def update_role(role_data, role_id):
#         role = RoleModel.query.get(role_id)
#         role.name = role_data['name']
#         db.session.add(role)
#         db.session.commit()
#         return role
#
#     @staticmethod
#     def get_all_roles():
#         all_roles = RoleModel.query.all()
#         return all_roles
#
#
