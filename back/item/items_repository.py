from ..common_imports import *
#from .items_service import create_model
from ..tag import PlainTagSchema, TagModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, ProgrammingError, DataError
from flask_smorest import abort
import jsonify
from ..utils import create_model


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
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ItemRepository:

    @staticmethod
    def get_item(item_id):
        return ItemModel.query.get_or_404(item_id)

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

    @staticmethod
    def add_tag(item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag in item.tags:
            return {"message": "Tag already associated with the item"}, 400

        item.tags.append(tag)

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Tag added to the item", "item": item, "tag": tag}


    @staticmethod
    def update_item(item_data, item_id):
        item = ItemModel.query.get(item_id)
        item.price = item_data['price']
        item.name = item_data['name']
        item.description = item_data['description']
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            error_message = str(error.orig)
            abort(500, message=error_message)
        except ProgrammingError as error:
            db.session.rollback()
            abort(500, message=error)

        except DataError as error:
            db.session.rollback()
            abort(500, message=error)
        except SQLAlchemyError as error:
            abort(500, message=error)
        return item

    @staticmethod
    def delete_item(item_id):
        item = ItemModel.query.get(item_id)
        db.session.delete(item)
        db.session.commit()


class ItemSchema(PlainItemSchema):
    pass

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(PlainItemSchema())
    #item = fields.Str()

    tag = fields.Nested(PlainTagSchema())


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    description = fields.Str()