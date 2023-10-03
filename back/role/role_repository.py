from ..common_imports import *
from ..location import PlainLocationSchema, LocationModel
from ..db import db
from ..utils import create_model

class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class PlainRoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)

class RoleRepository:
    @staticmethod
    def create(data):
        return create_model(RoleModel, data)

    @staticmethod
    def get_locations(organization_id):
        organization_locations = LocationModel.query.filter(LocationModel.organization_id == organization_id)
        return organization_locations
    @staticmethod
    def delete_organization(organization_id):
        organization = OrganizationModel.query.get(organization_id)
        db.session.delete(organization)
        db.commit()
    @staticmethod
    def update_organization(organization_data, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        organization.name = organization_data['name']
        db.session.add(organization)
        db.session.commit()
        return organization

    @staticmethod
    def get_all_roles():
        all_roles = RoleModel.query.all()
        return all_roles


