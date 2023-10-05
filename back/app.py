from flask import Flask
from flask_smorest import Api
from .db import db
from dotenv import load_dotenv
from .config import app_config
from flask_migrate import Migrate
from .organization import OrganizationBlueprint
from .location import LocationBlueprint, LocationModel
from .item import ItemBlueprint, ItemModel
from .qrs import QRBlueprint
from .traindata import IntentsBlueprint, PatternBlueprint, PatternModel
from .traindata import ResponseModel, ResponseBlueprint
from .tag import TagBlueprint, TagModel, ItemTags
from .category import CategoryBlueprint
from .chatbot import ChatBlueprint
from .user import UserBlueprint, TokenBlocklist
from flask_jwt_extended import JWTManager

import yaml
def create_app():
    app = Flask(__name__)

    load_dotenv()
    app_config(app)

    db.init_app(app)
    migrate = Migrate(app, db, table='MENUrasa/back/migrations')

    api = Api(app)

    api.register_blueprint(OrganizationBlueprint)
    api.register_blueprint(LocationBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(QRBlueprint)
    api.register_blueprint(IntentsBlueprint)
    api.register_blueprint(PatternBlueprint)
    api.register_blueprint(ResponseBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(ChatBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(UserBlueprint)

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    return app
# app = create_app()
# with app.app_context():
#     for response in bestellen_responses:
#         response_data = {
#             "response": response,
#             "intent_id": 24,
#             "language": "NL"
#         }
#         create_model(ResponseModel, response_data)
#app = create_app()
# with app.app_context():
#     location_id = '28f1b95a19d44b478dda48eb43ae3426'
#     query = db.session.query(ItemModel).join(LocationModel).filter(LocationModel.id == location_id)
#
#     # Execute the query and retrieve the items
#     items = query.all()
#
#     # Process the queried items
#     for item in items:
#         # Access the item data
#         item_id = item.id
#         item_name = item.name
#         # ... other item attributes
#         print(f"Item ID: {item_id}, Item Name: {item_name}")
#cleaned_text = text.encode("utf-8").decode("unicode_escape")

# with app.app_context():
#     intent_id = 23
#     names = ResponseModel.query.filter(ResponseModel.intent_id==intent_id).all()
#     name_list = [name.response for name in names]
#     #data = [{"intent": "gerecht_vragen", "examples": name_list}]
# #
#     with open('chatbot/data/domain.yml', 'r') as file:
#         data = yaml.safe_load(file)
#
#     for response in name_list:
#         data['responses']['utter_menu_kijken'].append({"text": response })
#     with open('chatbot/data/domain.yml', 'w') as file:
#         yaml.dump(data, file)
#
# #         yaml.dump(data, f)
# app = create_app()
# with app.app_context():
#     location_id = '28f1b95a19d44b478dda48eb43ae3426'
#     tag_names = TagModel.query. \
#         join(ItemTags). \
#         join(ItemModel). \
#         filter(ItemModel.location_id == location_id).all()
#
#     tag_name_list = [tag.name for tag in tag_names]
#     print(tag_name_list)