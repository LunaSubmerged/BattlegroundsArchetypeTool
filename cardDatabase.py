import json
import requests
import os

from enum import Enum
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

class CreatureType(Enum):
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

class Archetypes:
    def __init__(self, name: str, mandatoryTypes: list, minions: list, level: int, optionalTypes = {}, description = ""):
     self.name = self.__class.__name__
     self.mandatoryTypes = mandatoryTypes
     self.optionalTypes = optionalTypes
     self.description = description
     self.minions = minions
     self.level = level
    pass

class Card:
    def __init__(self, name, types, tier, image, duosOnly, solosOnly, id):
        self.name = name
        self.types = types
        self.tier = tier
        self.image = image
        self.duosOnly = duosOnly
        self.solosOnly = solosOnly
        self.archetypes = []
        self.id = id


def get_api_data():
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    token_response = requests.post(url = "https://oauth.battle.net/token", data={"grant_type" : "client_credentials"}, auth = HTTPBasicAuth(client_id, client_secret))
    token = token_response.json()["access_token"]
    url = "https://api.blizzard.com/hearthstone/cards?bgCardType=minion&gameMode=battlegrounds&pageSize=1000&locale=en_US"
    return requests.get(url = url, headers={"authorization" : f"Bearer {token}" }).json()

print("program running")
if __name__ == "__main__":
    load_dotenv()

    battlegrounds_card_dict = {}
    cards_list = get_api_data()["cards"]

    for card in cards_list:
        types = []
        if "minionTypeId" in card:
            types.append(CreatureType(card["minionTypeId"]))
        if "multiTypeIds" in card:
            types += [CreatureType(type) for type in card["multiTypeIds"]]
        if len(types) == 0:
            types.append(CreatureType.ALL)
        battlegrounds = card["battlegrounds"]
        local_card = Card(
            name= card["name"],
            types= types,
            tier= battlegrounds["tier"],
            image=battlegrounds["image"],
            duosOnly=battlegrounds["duosOnly"],
            solosOnly=battlegrounds["solosOnly"],
            id= card["id"]
                        )
        battlegrounds_card_dict[local_card.name] = local_card
