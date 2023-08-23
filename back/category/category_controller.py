from flask.views import MethodView
from .category_repository import CategoryModel, PlainCategorySchema, CategoryRepository
from flask_smorest import abort, Blueprint


blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/category")
class Category(MethodView):
    @blp.arguments(PlainCategorySchema)
    @blp.response(200, PlainCategorySchema)
    def post(self, category_data):
        category = CategoryRepository.create(category_data)
        return category
