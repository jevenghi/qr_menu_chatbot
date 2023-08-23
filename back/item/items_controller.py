from flask.views import MethodView
from .items_repository import ItemModel, PlainItemSchema, TagAndItemSchema
from .items_repository import ItemRepository
from flask_smorest import abort, Blueprint


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item")
class Item(MethodView):
    @blp.arguments(PlainItemSchema)
    @blp.response(200, PlainItemSchema)
    def post(self, item_data):
        item = ItemRepository.create(item_data)
        return item
    #
    # @blp.response(200, PlainLocationSchema(many=True))
    # def get(self):
    #     return LocationModel.query.all()
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class RemoveTag(MethodView):
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):




        deleted_tag = ItemRepository.delete_tag(item_id, tag_id)
        return deleted_tag

