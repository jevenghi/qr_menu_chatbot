from ..common_imports import *
from ..db import db
from ..utils import create_model

class QRModel(db.Model):
    __tablename__ = "qrs"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4().hex))
    organization_id = db.Column(
        "organizationId", db.String, db.ForeignKey("organizations.id"), nullable=False
    )
    location_id = db.Column(
        "locationId", db.String, db.ForeignKey("locations.id"), nullable=False
    )

    organization = db.relationship("OrganizationModel", back_populates="qrs")
    location = db.relationship("LocationModel", back_populates="qrs")

class PlainQRSchema(Schema):
    organization_id = fields.Str(data_key='organizationId', attribute='organization_id',required=True)
    location_id = fields.Str(data_key='locationId', attribute='location_id',required=True)

class QRRepository:
    @staticmethod
    def create(data):
        return create_model(QRModel, data)

