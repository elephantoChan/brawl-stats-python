import json

import requests


class Map:
    def __init__(self, name: str):
        data = requests.get("https://api.brawlify.com/v1/maps").json()["list"]
        for map_info in data:
            if map_info["name"].lower() == name.lower():
                self.id: int = map_info["id"]
                self.name: str = map_info["name"]
                self.link: str = map_info["link"]
                self.image: str = map_info["imageUrl"]
                self.gamemode_name: str = map_info["gameMode"]["name"]
                self.gamemode_color: str = map_info["gameMode"]["color"]
                self.exists = True
                return

        self.exists = False


class Brawler:
    def __init__(self, name: str):
        data = requests.get("https://api.brawlify.com/v1/brawlers").json()["list"]
        for b in data:
            if b["name"].lower() == name.lower():
                self.id: int = b["id"]
                self.name: str = b["name"]
                self.link: str = b["link"]
                self.image: str = b["imageUrl"]
                self.brawler_class: str = b["class"]["name"]
                self.rarity: str = b["rarity"]["name"]
                self.rarity_color: str = b["rarity"]["color"]
                self.description: str = b["description"]
                self.starpower_1_name: str = b["starPowers"][0]["name"]
                self.starpower_2_name: str = b["starPowers"][1]["name"]
                self.starpower_1_description: str = b["starPowers"][0]["description"]
                self.starpower_2_description: str = b["starPowers"][1]["description"]
                self.gadget_1_name: str = b["gadgets"][0]["name"]
                self.gadget_2_name: str = b["gadgets"][1]["name"]
                self.gadget_1_description: str = b["gadgets"][0]["description"]
                self.gadget_2_description: str = b["gadgets"][1]["description"]
                self.exists = True
                return

        self.exists = False


class Player:
    def __init__(self, tag: str):
        tag = tag.replace("#", "")
        conf = ""
        with open("env.json", "r") as f:
            data = json.loads(f.read())
            conf = data["brawl_token"]
        data = requests.get(
            f"https://bsproxy.royaleapi.dev/v1/players/%23{tag}",
            headers={"Authorization": f"Bearer {conf}"},
        )
        if data.status_code != 200:
            self.exists = False
            return
        data = data.json()
        self.exists: bool = True
        self.tag: str = data["tag"]
        self.name: str = data["name"]
        self.name_color = 12817901
        if "nameColor" in data:
            self.name_color: int = int(data["nameColor"][0:8], 16)
        self.icon: str = data["icon"]["id"]
        self.current_trophies: int = data["trophies"]
        self.highest_trophies: int = data["highestTrophies"]
        self.exp_level: int = data["expLevel"]
        self.victories_3v3: int = data["3vs3Victories"]
        self.victories_solo: int = data["soloVictories"]
        self.victories_duo: int = data["duoVictories"]
        self.club = {}
        self.is_in_club = False
        if "club" in data:
            if data["club"] != {}:
                self.is_in_club = True
                self.club = {"name": data["club"]["name"], "tag": data["club"]["tag"]}
        self.brawlers = []
        for brawler in data["brawlers"]:
            self.brawlers.append(PlayerBrawler(brawler))

    def __str__(self):
        if self.exists and self.is_in_club:
            return f"{self.name} is currently in {self.club['name']} at exp level {self.exp_level}"
        elif self.exists:
            return f"{self.name} not in a club, at exp level {self.exp_level}"
        else:
            return "Invalid tag."


class PlayerBrawler:
    def __init__(self, brawler: dict):
        self.id = brawler["id"]
        self.name = brawler["name"]
        self.power = brawler["power"]
        self.rank = brawler["rank"]
        self.current_trophies = brawler["trophies"]
        self.highest_trophies = brawler["highestTrophies"]
        self.gears = []
        self.star_powers = []
        self.gadgets = []
        for gear in brawler["gears"]:
            self.gears.append(PlayerBrawlerAccessory(gear))
        for star_power in brawler["starPowers"]:
            self.star_powers.append(PlayerBrawlerAccessory(star_power))
        for gadget in brawler["gadgets"]:
            self.gadgets.append(PlayerBrawlerAccessory(gadget))


class PlayerBrawlerAccessory:
    def __init__(self, accs: dict):
        self.id = accs["id"]
        self.name = accs["name"]
