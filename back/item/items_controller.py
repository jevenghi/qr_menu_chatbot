from flask.views import MethodView
from .items_repository import ItemModel, PlainItemSchema, TagAndItemSchema, ItemUpdateSchema
from .items_repository import ItemRepository
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required


blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item")
class Item(MethodView):
    #@jwt_required
    @blp.arguments(PlainItemSchema)
    @blp.response(201, PlainItemSchema)
    def post(self, item_data):
        item = ItemRepository.create(item_data)
        return item
    #
    # @blp.response(200, PlainLocationSchema(many=True))
    # def get(self):
    #     return LocationModel.query.all()

@blp.route("/item/<string:item_id>/tag/<int:tag_id>")
class ItemTag(MethodView):
    #@jwt_required
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        deleted_tag = ItemRepository.delete_tag(item_id, tag_id)
        return deleted_tag

    #@jwt_required
    @blp.response(200, TagAndItemSchema)
    def post(self, item_id, tag_id):
        added_tag = ItemRepository.add_tag(item_id, tag_id)
        return added_tag


@blp.route("/item/<string:item_id>")
class ItemCrud(MethodView):
    @blp.response(200, PlainItemSchema)
    def get(self, item_id):
        return ItemRepository.get_item(item_id)

    @jwt_required
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)

    #  The URL arguments come in at the end. ' \
    # 'The injected arguments are passed first, so item_data goes before item_id in our function signature.
    def put(self, item_data, item_id):
        item = ItemRepository.update_item(item_data, item_id)
        return item

    #@jwt_required
    def delete(self, item_id):
        ItemRepository.delete_item(item_id)
        return {'message': 'Item deleted successfully'}








