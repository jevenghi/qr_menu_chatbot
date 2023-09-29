from ..common_imports import *
from ..utils import create_model


class LocationModel(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4().hex))
    name = db.Column(db.String, unique=True)
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    organization_id = db.Column(
        "organizationId", db.String, db.ForeignKey("organizations.id"), unique=False, nullable=False
    )
    organization = db.relationship("OrganizationModel", back_populates="location")
    items = db.relationship("ItemModel", lazy="dynamic", back_populates="location")
    qrs = db.relationship("QRModel", back_populates="location")
    chatbots = db.relationship("ChatbotModel", back_populates="location")



class PlainLocationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)
    organization_id = fields.Str(data_key='organizationId', attribute='organization_id', required=True)


class LocationSchema(PlainLocationSchema):
    pass


class LocationRepository:
    @staticmethod
    def create(data):
        return create_model(LocationModel, data)

    @staticmethod
    def delete_location(location_id):
        location = LocationModel.query.get(location_id)
        db.session.delete(location)
        db.session.commit()


    @staticmethod
    def update_location(location_data, location_id):
        location = LocationModel.query.get(location_id)
        location.name = location_data['name']
        location.organization_id = location_data['organization_id']
        db.session.add(location)
        db.session.commit()
        return location



