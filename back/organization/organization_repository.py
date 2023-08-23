from ..common_imports import *
from ..location import PlainLocationSchema
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

