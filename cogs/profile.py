import datetime

from nextcord import Embed
from nextcord.ext import commands

from lib.api import Player
from log_help.log import log


class ProfileCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="profile")
    async def profile(self, context, *args):
        PLAYER = Player(args[0])
        log(
            f"User {context.author}({context.message.author.id}) used command [[{context.command} {context.args[2]}]]"
        )
        # Calculations here.
        season_reset: int = 0
        total_p11_brawlers: int = 0
        total_star_powers: int = 0
        total_gadgets: int = 0
        total_gears: int = 0
        pp_to_max: int = 0
        coins_to_max: int = 0
        for brawler in PLAYER.brawlers:
            if brawler.current_trophies > 1000:
                season_reset += brawler.current_trophies - 1000
            if brawler.power == 11:
                total_p11_brawlers += 1
            total_star_powers += len(brawler.star_powers)
            total_gadgets += len(brawler.gadgets)
            total_gears += len(brawler.gears)
            pp_to_max += fib_sum(brawler.power)
            coins_to_max += coin_sum(brawler.power)
            coins_to_max += (
                0
                if len(brawler.star_powers) == 2
                else 2000
                if len(brawler.star_powers) == 1
                else 4000
            )
            coins_to_max += (
                0
                if len(brawler.gadgets) == 2
                else 1000
                if len(brawler.gadgets) == 1
                else 2000
            )
            coins_to_max += (
                0
                if len(brawler.gears) >= 2
                else 1000
                if len(brawler.gears) == 1
                else 2000
            )

        embed: dict = {
            "color": PLAYER.name_color,
            "title": PLAYER.name,
            "description": f"{PLAYER}",
            "timestamp": f"{datetime.datetime.now(datetime.timezone.utc)}",
            "footer": {
                "text": "Progression numbers may be less than what is required.",
            },
            "thumbnail": {
                "url": f"https://cdn.brawlify.com/profile-icons/regular/{PLAYER.icon}.png"
            },
            "fields": [
                {
                    "name": "Trophies",
                    "value": f"<:BS_Trophy:1303802193580785766> **Current**:\n{PLAYER.current_trophies:,}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"<:BS_Trophy:1303802193580785766> **Trophies PB**:\n{PLAYER.highest_trophies:,}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"<:BS_Trophy:1303802193580785766> **Season Reset**\n{PLAYER.current_trophies - season_reset:,} (**{season_reset}** towards box)",
                    "inline": True,
                },
                {"name": "", "value": "", "inline": False},
            ],
        }

        # Club shit
        if PLAYER.is_in_club:
            embed["fields"].extend(
                [
                    {
                        "name": "Club Info",
                        "value": f"<:BS_Club:1303806687442108446> **Club**\n{PLAYER.club['name']}",
                        "inline": True,
                    },
                    {
                        "name": "\u200b",
                        "value": f"<:BS_Club:1303806687442108446> **Tag**\n{PLAYER.club['tag']}",
                        "inline": True,
                    },
                    {"name": "\u200b", "value": "\u200b", "inline": True},
                ]
            )

        # Victories
        embed["fields"].extend(
            [
                {
                    "name": "Victories",
                    "value": f"<:BS_3v3:1303802077180334100> **3v3 Wins**\n{PLAYER.victories_3v3:,}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"<:BS_Showdown:1303802043118522418> **Solo Wins**\n{PLAYER.victories_solo:,}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"<:BS_Showdown:1303802043118522418> **Duo Wins**\n{PLAYER.victories_duo:,}",
                    "inline": True,
                },
            ]
        )

        # Economy shit
        embed["fields"].extend(
            [
                {
                    "name": "<:BS_Stats:1303806056228720660> Stats",
                    "value": f"<:BS_LvlUp:1303802115113619547> **P11 Brawlers**\n{total_p11_brawlers}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"**Accessories**\n<:BS_starpower:1303801924856057901> {total_star_powers}\n<:BS_gadget:1303801867163271198> {total_gadgets}\n<:BS_gear:1303801901803896912> {total_gears}",
                    "inline": True,
                },
                {
                    "name": "\u200b",
                    "value": f"**Progression**\n<:BS_PowerPoint:1303943035452653568> {pp_to_max:,}\n<:BS_Coin:1303942959691202652> {coins_to_max:,}",
                    "inline": True,
                },
            ]
        )

        # Send
        await context.send(embed=Embed.from_dict(embed))


def setup(bot):
    bot.add_cog(ProfileCog(bot))


def fib_sum(n: int) -> int:
    if n == 11:
        return 0
    fib_sequence = [0, 1]
    for i in range(2, 12):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    if n < 0 or n > 11:
        raise Exception("What?")
    fib_sequence.pop(1)
    return sum(fib_sequence[n - 1 :]) * 10


def coin_sum(n: int) -> int:
    if n == 11:
        return 0
    sequence = [0, 20, 35, 75, 140, 290, 480, 800, 1250, 1875, 2800]
    return sum(sequence[n:])
