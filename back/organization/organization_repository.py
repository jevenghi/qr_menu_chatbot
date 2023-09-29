from ..common_imports import *
from ..location import PlainLocationSchema, LocationModel
from ..db import db
from ..utils import create_model

class OrganizationModel(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4().hex))
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    location = db.relationship("LocationModel", back_populates="organization")
    qrs = db.relationship("QRModel", back_populates="organization")


class PlainOrganizationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)


class OrganizationSchema(PlainOrganizationSchema):
    locations = fields.List(fields.Nested(PlainLocationSchema()), dump_only=True)

class OrganizationRepository:
    @staticmethod
    def create(data):
        return create_model(OrganizationModel, data)

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
    def get_all_organizations():
        all_organizations = OrganizationModel.query.all()
        return all_organizations


