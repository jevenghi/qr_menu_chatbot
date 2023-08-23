from ..common_imports import *
from ..utils import create_model


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    tags = db.relationship(
        "TagModel",
        secondary="category_tags",
        back_populates="categories", lazy="dynamic"
    )
    items = db.relationship(
        "ItemModel",
        back_populates="categories", lazy="dynamic"
    )

class CategoryTags(db.Model):
    __tablename__ = "category_tags"

    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Str(data_key='createdAt', attribute='created_at', dump_only=True)

class CategoryRepository:
    @staticmethod
    def create(data):
        return create_model(CategoryModel, data)