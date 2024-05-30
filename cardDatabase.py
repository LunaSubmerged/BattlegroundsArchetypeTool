import json
import requests
import os
import archetype

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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


class CardDatabase:

    def __init__(self):
        self.battlegrounds_card_dict = {}
        cards_list = self.get_api_data()["cards"]

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
            self.battlegrounds_card_dict[local_card.name] = local_card


    def get_api_data(self):
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")
        token_response = requests.post(url = "https://oauth.battle.net/token", data={"grant_type" : "client_credentials"}, auth = HTTPBasicAuth(client_id, client_secret))
        token = token_response.json()["access_token"]
        url = "https://api.blizzard.com/hearthstone/cards?bgCardType=minion&gameMode=battlegrounds&pageSize=1000&locale=en_US"
        return requests.get(url = url, headers={"authorization" : f"Bearer {token}" }).json()
    
    def getMinion(self,name: str):
        l_name = name.lower()
        fuzzy = process.extract(name, self.battlegrounds_card_dict.keys(), limit = 1)
        fuzzyName = fuzzy[0][0]

        if fuzzyName in self.battlegrounds_card_dict:
            return (self.battlegrounds_card_dict[fuzzyName])
        
    def getMinions(self,*names: str):
        minions = []
        for name in names:
            minions.append(self.getMinion(name))
        return minions

if __name__ == "__main__":
    load_dotenv()
    cardDatabase = CardDatabase()

    undead_attack_stacking = archetype.Archetype(
        name= "Undead Attack Stacking",
        mandatoryTypes=[CreatureType.UNDEAD],
        optionalTypes=[CreatureType.BEAST, CreatureType.MECH, CreatureType.MURLOC],
        coreMinions=cardDatabase.getMinions("Archlinch Kel'Thuzad", "hateful hag", "handless forsaken"),
        optionalMinions=cardDatabase.getMinions("nerubian deathswarmer", "murgl mk II"),
        tier=5,
        description="Stack permanent attack buffs on your undead, use deathrattle and reborn to attack numerous times."
    )

    undead_attack_stacking.printArchetypeInfo()
