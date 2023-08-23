from ..common_imports import *
from ..utils import create_model


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    # location_id = db.Column("locationId", db.String, db.ForeignKey("locations.id"))
    # location = db.relationship("LocationModel", back_populates="tags")
    items = db.relationship(
        "ItemModel",
        secondary="items_tags",
        back_populates="tags", lazy="dynamic"
    )
    categories = db.relationship(
        "CategoryModel",
        secondary="category_tags",
        back_populates="tags", lazy="dynamic"
    )


class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))


class PlainTagSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    # created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)


class TagRepository:
    @staticmethod
    def create(data):
        return create_model(TagModel, data)




