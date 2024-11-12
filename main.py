import json
import os

import nextcord
from nextcord.ext import commands

from log_help.log import log


class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.add_commands()
        self.load_cogs()

    def add_commands(self):
        @self.command(name="ping")
        async def ping(ctx):
            """Replies with the bot's latency"""
            latency = round(self.latency * 1000)
            await ctx.send(f"Current latency: {latency}ms")

    def load_cogs(self):
        """
        Load all cogs from the 'cogs' folder.
        """
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                cog_name = filename[:-3]
                try:
                    self.load_extension(f"cogs.{cog_name}")
                    log(f"Loaded cog: {cog_name}")
                except Exception as e:
                    log(f"Failed to load cog {cog_name}: {e}", level="ERROR")

    async def on_ready(self):
        log(f"Logged in as {self.user}")


intents = nextcord.Intents.default()
intents.message_content = True
client = MyBot("bs ", intents=intents)

token = ""
with open("env.json", "r") as config:
    data = json.loads(config.read())
    token = data["test_discord_token"]
client.run(token)
