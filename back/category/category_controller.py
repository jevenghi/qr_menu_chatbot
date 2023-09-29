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

    @blp.response(200, PlainCategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()




@blp.route("/category/<int:category_id>")
class CategoryGUD(MethodView):
    def delete(self, category_id):
        CategoryRepository.delete_category(category_id)
        return {'message': f'Category deleted successfully'}

    @blp.arguments(PlainCategorySchema)
    @blp.response(200, PlainCategorySchema)
    def put(self, data, category_id):
        category = CategoryRepository.update_category(data, category_id)
        return category

    @blp.response(200, PlainCategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(category_id)



