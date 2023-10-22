from flask.views import MethodView
from .tag_repository import TagModel, PlainTagSchema
from flask_smorest import abort, Blueprint
from .tag_repository import TagRepository
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/tag")
class Tag(MethodView):

    #@jwt_required()
    @blp.arguments(PlainTagSchema)
    @blp.response(201, PlainTagSchema)
    def post(self, tag_data):
        tag = TagRepository.create(tag_data)
        return tag

    #@jwt_required()
    @blp.response(200, PlainTagSchema(many=True))
    def get(self):
        return TagRepository.get_all_tags()


@blp.route("/tag/<int:tag_id>")
class TagGUD(MethodView):
    @blp.response(200, PlainTagSchema)
    def get(self, tag_id):
        return TagRepository.get_tag(tag_id)

    @jwt_required()
    @blp.arguments(PlainTagSchema)
    @blp.response(200, PlainTagSchema)
    def put(self, tag_data, tag_id):
        updated_tag = TagRepository.update_tag(tag_data, tag_id)
        return updated_tag

    @jwt_required()
    def delete(self, tag_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        TagRepository.delete_tag(tag_id)
        return {'message': 'Tag deleted successfully'}
