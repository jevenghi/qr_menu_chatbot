from ..common_imports import *
from .items_service import create_model
from ..tag import PlainTagSchema, TagModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, ProgrammingError, DataError
from flask_smorest import abort

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4().hex))
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    location_id = db.Column("locationId", db.String, db.ForeignKey("locations.id"), nullable=False)
    description = db.Column(db.String)
    available = db.Column(db.Boolean)
    location = db.relationship("LocationModel", back_populates="items")
    category_id = db.Column("categoryId", db.Integer, db.ForeignKey("categories.id"), nullable=False)
    categories = db.relationship("CategoryModel", back_populates="items")
    tags = db.relationship(
        "TagModel",
        secondary="items_tags",
        back_populates="items", lazy="dynamic"
    )

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)
    location_id = fields.Str(data_key='locationId', attribute='location_id', required=True)
    category_id = fields.Int(data_key='categoryId', attribute='category_id', required=True)
    description = fields.Str()
    #tags = fields.List(fields.Int())
    tags = fields.List(fields.Nested(PlainTagSchema()), required=True)


class ItemRepository:
    @staticmethod
    def create(data):
        return create_model(ItemModel, data)

    @staticmethod
    def delete_tag(item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Tag not associated with the item")

        return {"message": "Tag removed from item", "item": item, "tag": tag}


class ItemSchema(PlainItemSchema):
    pass

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(PlainItemSchema())
    tag = fields.Nested(PlainTagSchema())