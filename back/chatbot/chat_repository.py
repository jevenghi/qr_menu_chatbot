from ..common_imports import *
from ..utils import create_model
from fuzzywuzzy import fuzz
import re
from ..tag import TagModel, ItemTags
from ..item import ItemModel
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload


class ChatbotModel(db.Model):
    __tablename__ = "chatbots"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4().hex))
    created_at = db.Column("createdAt", db.DateTime, default=datetime.now)
    location_id = db.Column("locationId", db.String, db.ForeignKey("locations.id"), nullable=False)
    location = db.relationship("LocationModel", back_populates="chatbots")
    user_input = db.Column(db.String)

class PlainChatbotSchema(Schema):

    location_id = fields.Str(data_key='locationId', attribute='location_id', required=True)
    user_input = fields.Str()


class ChatbotSchema(Schema):
    message = fields.Str()



class ChatbotRepository:
    @staticmethod
    def create(data):
        return create_model(ChatbotModel, data)

    @staticmethod
    def all_tags(tags_matched):
        query = ItemModel.query.join(ItemModel.tags).filter(TagModel.name.in_(tags_matched))

        # ensure that only items with exactly the specified tags are retrieved
        query = query.group_by(ItemModel.id).having(and_(db.func.count(TagModel.id) == len(tags_matched)))
        items_with_exact_tags = query.all()

        item_names = [item.name for item in items_with_exact_tags]
        return {"match": "full", "items": item_names}

    @staticmethod
    def tags(tags_raw, location_id):
        pattern = r'ger.*'
        tags_sep = [re.sub(pattern, "", tag_name) for tag_name in tags_raw]

        location_tags = TagModel.query. \
            join(ItemTags). \
            join(ItemModel). \
            filter(ItemModel.location_id == location_id).all()
        location_tag_names = [tag.name.lower() for tag in location_tags]

        # all_tags = TagModel.query.all()
        # all_tag_names = [tag.name.lower() for tag in all_tags]

        #Creates a list of tags from user input which exist in the location tags list, using fuzz ratio for handling typos
        tags_matched = [loc_tag for tag in tags_sep for loc_tag in location_tag_names if fuzz.ratio(tag, loc_tag) >= 80]
        if len(tags_sep) == len(tags_matched):
            return ChatbotRepository.all_tags(tags_matched)

        elif tags_matched and len(tags_matched) < len(tags_sep):
            tags_ids_objs = TagModel.query.filter(
                TagModel.name.in_(tags_matched)
            ).all()
            tags_ids = [tag.id for tag in tags_ids_objs]

            return ChatbotRepository.any_tag(tags_ids, location_id)
        else:
            return {"match": "null"}

        #return tags_matched, tags_ids



    @staticmethod
    def any_tag(tags_ids, location_id):
        clauses = [ItemTags.tag_id == tag_id for tag_id in tags_ids]
        items = (
            ItemModel.query
            .join(ItemTags)
            .filter(
                ItemModel.location_id == location_id,
                or_(*clauses)
            )
            .all()
        )

        item_names = [item.name for item in items]
        return {"match": "partial", "items": item_names}

    @staticmethod
    def get_cat(category, location_id):
        if category == "voorgerecht":
            items = ItemModel.query.filter(
                ItemModel.location_id == location_id,
                ItemModel.category_id == 2
            ).all()

            return [item.name for item in items]

        if category == "hoofdgerecht":
            items = ItemModel.query.filter(
                ItemModel.location_id == location_id,
                ItemModel.category_id == 1
            ).all()

            return [item.name for item in items]