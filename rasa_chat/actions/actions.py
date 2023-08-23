# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import fuzz
# from back.item import ItemModel
# from back.chatbot import ChatbotModel
# from .menu_items import menu
import requests
from rasa_sdk.events import SlotSet


class ActionCheckDishMenu(Action):

    def name(self) -> Text:
        return "action_check_dish_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dish_name = next(tracker.get_latest_entity_values("dish_name"))
        chat_id = tracker.sender_id

        backend_url = f"http://localhost:5000/chat/{chat_id}"
        menu = requests.get(backend_url).json()
        dish_name = tracker.get_slot("dish_name")

        if max((fuzz.ratio(dish_name, dish) for dish in menu)) >= 80:
            dispatcher.utter_message(text=f"Ja, we hebben {dish_name} op het menu.")
        alternative_dishes = [dish for dish in menu if (fuzz.ratio(dish_name, dish)) > 50]
        if alternative_dishes:
            dispatcher.utter_message(text=f"Helaas hebben we geen {dish_name} op het menu. "
                                          f"Er zijn wel andere alternatieven {alternative_dishes}")
        else:
            dispatcher.utter_message(text=f"Helaas hebben we geen {dish_name} op het menu. "
                                          f"Kan ik u helpen met een ander gerecht?")
        # dispatcher.utter_message(text=menu)
        return []


class ActionCheckTag(Action):

    def name(self) -> Text:
        return "action_check_tag"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dish_name = next(tracker.get_latest_entity_values("dish_name"))
        chat_id = tracker.sender_id
        #tag_name = tracker.get_slot("tag_name")
        entities = tracker.latest_message.get('entities', [])

        tag_names = [entity['value'] for entity in entities if entity['entity'] == 'tag']

        #backend_url = f"http://localhost:5000/chat/{chat_id}/tag/{tag_name}"
        backend_url = f"http://localhost:5000/chat/{chat_id}/tags"
        payload = {'tags': tag_names}
        items = requests.post(backend_url, json=payload).json()

        if items["match"] == "full":
            dispatcher.utter_message(text=f"Ja wij hebben gerechten met {' en '.join(tag_names)} op het menu: {items['items']}")
        if items["match"] == "partial":
            dispatcher.utter_message(text=f"Wij hebben wel gerechten met {' of '.join(tag_names)}. Hiervan mag U kiezen: {items['items']}.")
        else:
            dispatcher.utter_message(text=f"Helaas hebben we geen {' of '.join(tag_names)} op het menu. "
                                          f"Kan ik u helpen met een ander gerecht?")

        return []

class ActionShowByCategory(Action):

    def name(self) -> Text:
        return "action_show_by_cat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chat_id = tracker.sender_id
        intent_name = tracker.latest_message['intent']['name']
        backend_url = f"http://localhost:5000/chat/{chat_id}/category"
        payload = {"category": intent_name}
        items = requests.post(backend_url, json=payload).json()

        if items:
            dispatcher.utter_message(text=f"U mag kiezen: {items}")
        else:
            dispatcher.utter_message(text=f"Helaas hebben wij geen {intent_name}")





        return []