from flask.views import MethodView
from flask_smorest import abort, Blueprint
from ..item import ItemModel, PlainItemSchema
from .chat_repository import ChatbotSchema, ChatbotModel, ChatbotRepository, PlainChatbotSchema
from .chat_service import ChatbotService
from ..tag import TagModel, ItemTags
from flask import request
import requests
from fuzzywuzzy import fuzz
import re
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload


blp = Blueprint("chats", __name__, description="Operations on chats")

@blp.route("/chat")
class WelcomeChatbot(MethodView):
    @blp.arguments(PlainChatbotSchema)
    @blp.response(200, ChatbotSchema)
    def post(self, data):
        #
        # location_items = ItemModel.query.filter(ItemModel.location_id == location_id)
        # chat = ChatbotModel(location_id)
        # if chat.state == chat.welcome_state:
        #     message = chat.greet_customer()
        #     chat.state = chat.predict_state
        # #return [item.name for item in chat.menu]
        #     return {"message": message}
        # chat.predict_state(user_input)
        chat = ChatbotRepository.create(data)
        return {"message": "Hartelijk welkom! Ik ben Juna, uw Digitaal Ober, hoe kan ik u van dienst zijn?"}


@blp.route("/chat/<string:chat_id>")
class Chat(MethodView):
    @blp.response(200, ChatbotSchema)
    def post(self, chat_id):
        chat = ChatbotModel.query.get(chat_id)
        location_id = chat.location_id
        # location_items = ItemModel.query.filter(ItemModel.location_id == location_id)
        # menu = [item.name for item in location_items]

        user_input = request.json["user_input"]
        rasa_webhook_url = "http://192.168.2.6:5005/webhooks/rest/webhook"
        # rasa_webhook_url = "http://rasa_chat:5005/webhooks/rest/webhook"
        rasa_response = requests.post(rasa_webhook_url, json={"sender": chat.id, "message": user_input,
                                                              "location_id": location_id})

        # Extract the Rasa response and generate the appropriate response
        rasa_response_data = rasa_response.json()
        chatbot_reply = rasa_response_data[0][
            "text"] if rasa_response_data else "Sorry, I couldn't understand your request."

        return {"message": chatbot_reply}
        # return {"message": rasa_response_data}

    def get(self, chat_id):
        chat = ChatbotModel.query.get(chat_id)
        location_id = chat.location_id
        location_items = ItemModel.query.filter(ItemModel.location_id == location_id)
        menu = [item.name for item in location_items]
        # tags_objects = TagModel.query(TagModel.name).all()
        # tags = [name[0] for name in tags_objects]

        # tag_names = TagModel.query.join(ItemModel, ItemTags, TagModel).\
        #     filter(ItemModel.location_id == location_id).all()

        # tag_name_list = [tag.name for tag in tag_names]
        tag_names = TagModel.query. \
            join(ItemTags). \
            join(ItemModel). \
            filter(ItemModel.location_id == location_id).all()
        tag_name_list = [tag.name for tag in tag_names]

        return menu


@blp.route("/chat/<string:chat_id>/tags")
class Tags(MethodView):
    def post(self, chat_id):
        chat = ChatbotModel.query.get(chat_id)
        location_id = chat.location_id
        tags_raw = request.get_json()["tags"]

        return ChatbotRepository.tags(tags_raw, location_id)

@blp.route("/chat/<string:chat_id>/category")
class Tags(MethodView):
    def post(self, chat_id):
        chat = ChatbotModel.query.get(chat_id)
        location_id = chat.location_id
        category = request.get_json()["category"]

        return ChatbotRepository.get_cat(category, location_id)