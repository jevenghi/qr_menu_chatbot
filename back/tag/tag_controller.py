from flask.views import MethodView
from .tag_repository import TagModel, PlainTagSchema
from flask_smorest import abort, Blueprint
from .tag_repository import TagRepository


blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/tag")
class Tag(MethodView):
    @blp.arguments(PlainTagSchema)
    @blp.response(200, PlainTagSchema)
    def post(self, tag_data):
        tag = TagRepository.create(tag_data)
        return tag



