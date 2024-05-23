import json
import requests
import enum
import os

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

class CreatureType(enum.Enum):
    UNDEAD = 11
    MURLOC = 14
    DEMON = 15
    MECH = 17
    ELEMENTAL = 18
    BEAST = 20
    PIRATE = 23
    DRAGON = 24
    ALL = 26
    QUILLBOAR = 43
    NAGA = 92

class Archetypes():
    pass

class Card:
    def __init__(self, name, types, tier, image, duosOnly, solosOnly, archetypes, id):
        self.name = name
        self.types = types
        self.tier = tier
        self.image = image
        self.duosOnly = duosOnly
        self.solosOnly = solosOnly
        self.archetypes = archetypes
        self.id = id


load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
token_response = requests.post(url = "https://oauth.battle.net/token", data={"grant_type" : "client_credentials"}, auth = HTTPBasicAuth(client_id, client_secret))
token = token_response.json()["access_token"]
api_response = requests.get(url = "https://api.blizzard.com/hearthstone/cards?bgCardType=minion&gameMode=battlegrounds&pageSize=1000&locale=en_US", headers={"authorization" : f"Bearer {token}" })
print(json.dumps(api_response.json(), indent=4))
cards_list = api_response.json()["cards"]
battlegrounds_card_dict = {}
for card in cards_list:
    types = []
    if "minionTypeId" in card:
        types.append(CreatureType(card["minionTypeId"]))
    if "multiTypeIds" in card:
        types += [CreatureType(type) for type in card["multiTypeIds"]]
    if len(types) == 0:
        types.append(CreatureType.ALL)
    
    types = [CreatureType(card["minionTypeId"])]

    card[]
    local_card = Card(
        name = card["name"],
        types= []
                      )

