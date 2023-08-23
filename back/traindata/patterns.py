from ..common_imports import *
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from ..utils import create_model

blp = Blueprint("patterns", __name__, description="Operations on patterns")


class PatternModel(db.Model):
    __tablename__ = "patterns"

    id = db.Column(db.Integer, primary_key=True)
    pattern = db.Column(db.String)
    intent_id = db.Column("intentid", db.Integer, db.ForeignKey("intents.id"), nullable=False)
    language = db.Column(db.String(2), nullable=False)
    intent = db.relationship("IntentModel", back_populates="patterns")


class PatternSchema(Schema):
    id = fields.Str(dump_only=True)
    pattern = fields.Str(required=True)
    intent_id = fields.Int(data_key='intentid', attribute='intent_id', required=True)
    language = fields.Str(required=True)


@blp.route("/patterns")
class Pattern(MethodView):
    @blp.arguments(PatternSchema)
    @blp.response(200, PatternSchema)
    def post(self, pattern_data):
        pattern = create_model(PatternModel, pattern_data)
        return pattern


groeten_patterns = [
    "Hallo!",
    "Goedemorgen!",
    "Hoi!",
    "Dag!",
    "Goeiedag!",
    "Goedenavond!",
    "Hey!",
    "Goedendag!",
    "Goeiemiddag!",

]
menu_patterns = [
    "Mag ik de menukaart bekijken?",
    "Kunt u mij alstublieft een exemplaar van de menukaart geven?",
    "Heeft u een menu beschikbaar?",
    "Kan ik de menu-opties zien?",
    "Mag ik weten wat er op het menu staat?",
    "Kunt u mij vertellen welke gerechten er beschikbaar zijn?",
    "Heeft u een lijst met gerechten die ik kan bekijken?",
    "Kan ik de menu-opties en prijzen zien?",
    "Graag de menukaart om mijn bestelling te kiezen.",
    "Kunt u mij adviseren waar ik de menukaart kan vinden?",
    "Kan ik een blik werpen op het menu?",
    "Zou ik alsjeblieft de menu-opties kunnen bekijken?",
    "Heeft u een menu beschikbaar waar ik doorheen kan bladeren?",
    "Mag ik de menukaart even lenen om mijn keuze te maken?",
    "Kunt u mij laten zien welke gerechten er op het menu staan?",
    "Graag de menu-opties en eventuele speciale aanbiedingen, alstublieft.",
    "Kan ik de volledige menukaart zien, inclusief drankjes?",
    "Zou ik de menu-opties en prijzen kunnen inzien voordat ik mijn bestelling plaats?",
    "Heeft u een menukaart met vegetarische of veganistische opties?",
    "Mag ik de menukaart raadplegen om mijn voorkeur te bepalen?",
    "Kan ik de lijst met gerechten zien?",
    "Kunt u mij de beschikbare gerechten laten zien?",
    "Is er een menukaart die ik kan inzien?",
    "Mag ik de menu-opties bekijken voordat ik mijn keuze maak?",
    "Heeft u een overzicht van de gerechten?",
    "Waar kan ik de menukaart vinden?",
    "Kunt u mij helpen met het kiezen van een gerecht van het menu?",
    "Kan ik de menukaart raadplegen voor vegetarische opties?",
    "Mag ik de lijst met beschikbare gerechten bekijken?",
    "Heeft u een menukaart met gluten- of lactosevrije opties?",
    "Kan ik de menu-opties en hun prijzen zien?",
    "Graag de menukaart om mijn bestelling te plaatsen.",
    "Zou ik de lijst met gerechten kunnen zien?",
    "Wat zijn de specialiteiten van het huis?",
    "Kan ik de menukaart bekijken voordat ik een keuze maak?",
    "Heeft u een menukaart met kindermenu-opties?",
    "Mag ik het menu zien voordat ik mijn bestelling plaats?",
    "Zou ik de menu-opties en hun ingrediënten kunnen inzien?",
    "Kan ik de beschikbare gerechten bekijken?",
    "Heeft u een menu met seizoensgebonden gerechten?",
    "Kan ik de menukaart raadplegen om mijn dieetvoorkeuren te controleren?",
    "Mag ik de lijst met vegetarische gerechten zien?",
    "Heeft u een menu met veganistische opties?",
    "Kunt u mij de menu-opties en aanbevelingen geven?",
    "Graag de menukaart om mijn maaltijd te kiezen.",
    "Zou ik de lijst met drankjes kunnen zien?",
    "Wat zijn de populairste gerechten op het menu?",
    "Kan ik de menukaart inzien voor gezonde opties?",
]
bestellen_patterns = [
    "Ik wil graag de kipsalade bestellen.",
    "Kunt u voor mij een stuk appeltaart regelen?",
    "Mag ik een portie nacho's bestellen, alstublieft?",
    "Ik zou graag een vegetarische pizza willen bestellen.",
    "Kan ik de zalmfilet bestellen?",
    "Graag een club sandwich ontvangen, alstublieft.",
    "Kunt u mij een plak cheesecake bezorgen?",
    "Ik wil graag een portie sushi bestellen.",
    "Mag ik een bord spaghetti bestellen?",
    "Kan ik de vegetarische burger bestellen?",
    "Ik zou graag een kom tomatensoep willen hebben.",
    "Kunt u voor mij een stuk chocoladetaart aanschaffen?",
    "Ik wil graag een portie loempia's bestellen, als dat mogelijk is.",
    "Mag ik alstublieft een biefstuk bestellen?",
    "Kan ik de garnalencocktail opvragen?",
    "Ik wil graag een Caesar-salade aanschaffen.",
    "Kunt u mij een stuk carrot cake bezorgen, alstublieft?",
    "Ik zou graag een portie saté willen ontvangen.",
    "Mag ik een bord lasagne opvragen?",
    "Kan ik alsjeblieft de kipburger bestellen?",
    "Graag een margherita-pizza ontvangen, alstublieft.",
    "Kunt u voor mij een stuk bosbessentaart regelen?",
    "Ik wil graag een portie zoete aardappelfriet bestellen, alstublieft.",
    "Mag ik een bord pad thai opvragen?",
    "Kan ik de veggie wrap bestellen?",
    "Ik zou graag een portie groentesoep willen hebben.",
    "Kunt u mij een stuk red velvet cake bezorgen, alstublieft?",
    "Ik wil graag een portie dim sum bestellen, als dat mogelijk is.",
    "Mag ik alstublieft een schnitzel bestellen?",
    "Kan ik de tonijnsalade opvragen?",
    "Ik wil graag een Caprese-salade aanschaffen.",
    "Kunt u mij een plak appeltaart aanvragen?",
    "Ik zou graag een portie springrolls willen opvragen.",
    "Mag ik een bord carbonara bestellen?",
    "Kan ik de champignonburger bestellen?",
    "Ik wil graag een portie gazpacho aanschaffen.",
    "Kunt u voor mij een stuk tiramisu bezorgen?",
    "Ik wil graag een portie hummus bestellen.",
    "Mag ik een bord risotto opvragen?",
    "Kan ik de quinoasalade bestellen?",
    "Ik zou graag een portie miso-soep willen hebben.",
    "Kunt u mij een stuk key lime pie bezorgen, alstublieft?",
    "Ik wil graag een portie edamame bestellen, als dat mogelijk is.",
    "Mag ik alstublieft een kipsaté bestellen?",
    "Kan ik de garnalenrisotto opvragen?",
    "Ik wil graag een portie tabouleh aanschaffen.",
    "Kunt u mij een plak worteltaart aanvragen?",
    "Ik zou graag een portie kimchi willen opvragen.",
    "Mag ik een bord gnocchi bestellen?",
    "Kan ik de vegetarische curry bestellen?"
]


