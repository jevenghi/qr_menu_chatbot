from flask.views import MethodView
from .location_repository import LocationModel, PlainLocationSchema
from flask_smorest import abort, Blueprint
from .location_repository import LocationRepository
from ..item import PlainItemSchema, ItemModel
from flask_jwt_extended import jwt_required, get_jwt


blp = Blueprint("locations", __name__, description="Operations on locations")


@blp.route("/location")
class Location(MethodView):
    @jwt_required
    @blp.arguments(PlainLocationSchema)
    @blp.response(200, PlainLocationSchema)
    def post(self, location_data):
        location = LocationRepository.create(location_data)
        return location

    @jwt_required
    @blp.response(200, PlainLocationSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        return LocationModel.query.all()


@blp.route("/location/<string:location_id>")
class LocationItems(MethodView):
    @blp.response(200, PlainItemSchema(many=True))
    def get(self, location_id):
        location_items = ItemModel.query.filter(ItemModel.location_id == location_id)
        return location_items

    @jwt_required
    def delete(self, location_id):
        LocationRepository.delete_location(location_id)
        return {'message': 'Location deleted successfully'}

    @jwt_required
    @blp.arguments(PlainLocationSchema)
    @blp.response(200, PlainLocationSchema)
    def put(self, location_data, location_id):
        location = LocationRepository.update_location(location_data, location_id)
        return location




