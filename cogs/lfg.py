import datetime

import nextcord
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput

from lib.api import Map


class LfgCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(
        name="lfg", description="Add an advertisement in this channel!"
    )
    async def lfg(self, interaction: nextcord.Interaction):
        modal = LFGModal()
        await interaction.response.send_modal(modal)


def setup(bot):
    bot.add_cog(LfgCog(bot))


class LFGModal(Modal):
    def __init__(self):
        super().__init__(title="Looking for group")
        self.tag = TextInput(
            label="Your tag",
            placeholder="Your player tag here",
            required=True,
            max_length=12,
            style=nextcord.TextInputStyle.short,
        )
        self.map_name = TextInput(
            label="Map",
            placeholder="Map name here",
            required=True,
            max_length=30,
            style=nextcord.TextInputStyle.short,
        )
        self.players = TextInput(
            label="Amount of players needed here",
            placeholder="420",
            required=True,
            max_length=3,
            style=nextcord.TextInputStyle.short,
        )
        self.trophy_range = TextInput(
            label="Trophy/Rank range",
            placeholder="Eg: 45000-55000 or Diamond II - Masters",
            required=True,
            max_length=50,
            style=nextcord.TextInputStyle.short,
        )
        self.game_room_id = TextInput(
            label="Game room ID",
            placeholder="Room ID here",
            required=True,
            max_length=15,
            style=nextcord.TextInputStyle.short,
        )
        self.add_item(self.tag)
        self.add_item(self.map_name)
        self.add_item(self.trophy_range)
        self.add_item(self.players)
        self.add_item(self.game_room_id)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        tag = self.tag.value
        map_name = self.map_name.value
        trophies = self.trophy_range.value
        players = self.players.value
        room_id = self.game_room_id.value
        maap = Map(map_name)
        if not maap.exists:
            interaction.response.send_message(
                f"Error! Map {map_name} does not exist.", ephemeral=True
            )
            return

        embed = {
            "title": "Looking for group",
            "description": f"{interaction.user.name} ``{tag}`` wants to team up!\n\n[Click here to join!](https://youtube.com/)",
            "color": 12817901,
            "timestamp": f"{datetime.datetime.now(datetime.timezone.utc)}",
            "fields": [
                {
                    "name": "<:BS_Trophy:1303802193580785766> Required Trophies/Ranked League",
                    "value": f"{trophies}",
                },
                {"name": "Map", "value": f"[{maap.name}]({maap.link})"},
                {"name": "Players needed", "value": f"{players}"},
            ],
        }
        await interaction.followup.send(embed=nextcord.Embed.from_dict(embed))
