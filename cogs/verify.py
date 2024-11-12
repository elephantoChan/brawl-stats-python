import asyncio
import json
from random import randrange

from nextcord import Embed
from nextcord.ext import commands

from lib.api import Player
from log_help.log import log


class VerifyCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="verify")
    async def verify(self, ctx, *args):
        pl = Player(args[0])
        if not pl.exists:
            await ctx.send("Invalid player tag, please try again.", delete_after=5)
            return
        with open("database/users.json", "r") as f:
            data = json.loads(f.read())
            for user in data:
                if pl.tag == user["tag"] or ctx.author.id == user["discord_id"]:
                    await ctx.send(
                        f"<@{ctx.author.id}> Account already registered with tag: ``{user['tag']}``",
                        delete_after=5,
                    )
                    log(
                        f"User Verification was started for {ctx.author} ({ctx.author.id}) but user is already in database."
                    )
                    return
        log(f"User Verification started for {ctx.author} ({ctx.author.id})")
        icon_num = 28000000 + randrange(0, 50)
        if icon_num == pl.icon:
            icon_num -= 1 if icon_num != 228000000 else -1
        embed = {
            "title": "Verification",
            "color": 0x5AA2E0,
            "description": f"Verification has started for account name: **{pl.name}** `{pl.tag}`\nPlease follow the instructions below:\n1. Change your **in-game** player icon to the icon shown on the right.\n2. After changing your player icon, please wait for 1-2 minutes. You will receive a confirmation if the verification was successful.\n3. After the verification is complete, you may change your player icon back. \n\nIf you entered the wrong player tag, just wait and re-enter the tag after a few minutes.",
            "thumbnail": {
                "url": f"https://cdn.brawlify.com/profile-icons/regular/{icon_num}.png"
            },
            "footer": {
                "text": "If it did not work, please wait a few minutes and try again."
            },
        }
        await ctx.send(
            f"<@{ctx.author.id}>", embed=Embed.from_dict(embed), delete_after=90
        )
        count = 0
        tasks: set = set()
        stop = False
        while count <= 7 and not stop:
            task = asyncio.create_task(self.retrieve_player(pl.tag, icon_num, ctx))
            tasks.add(task)

            def task_done_callback(t):
                tasks.discard(t)
                nonlocal stop
                if t.result() is True:
                    stop = True
                    for running_task in tasks:
                        running_task.cancel()

            task.add_done_callback(task_done_callback)
            print("Sleeping Zzz...", count)
            await asyncio.sleep(10)
            count += 1
        await asyncio.gather(*tasks, return_exceptions=True)

    async def retrieve_player(self, *args):
        pl = Player(args[0])
        if pl.icon == args[1]:
            log(
                f"Verification Success: {pl.name} for {args[2].author}. Stopping check-loop."
            )
            await self.on_verification_complete(pl.tag, args[2])
            return True
        return False

    async def on_verification_complete(self, *args):
        data: list = []
        with open("database/users.json", "r") as f:
            data = json.loads(f.read())
            for obj in data:
                if args[0] == obj["tag"]:
                    return

        with open("database/users.json", "w") as f:
            data.append(
                {
                    "tag": args[0],
                    "discord_id": args[1].author.id,
                    "discord_name": args[1].author.name,
                }
            )
            f.write(json.dumps(data))
        await args[1].send(
            f"<@{args[1].author.id}> Verification success.", delete_after=10
        )


def setup(bot):
    bot.add_cog(VerifyCog(bot))
