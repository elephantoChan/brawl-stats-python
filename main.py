import os

import nextcord
from nextcord.ext import commands

from config_log.config import Config
from config_log.log import Log
from config_log.log import LogLevels as ll

logging = Log()  # Why am I even doing this :(


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
                    logging.log(f"Loaded cog: {cog_name}", level=ll.info)
                except Exception as e:
                    logging.log(f"Failed to load cog {cog_name}: {e}", level=ll.err)

    async def on_ready(self):
        logging.log(f"Logged in as {self.user} (ID: {self.user.id})", level=ll.info)


intents = nextcord.Intents.default()
intents.message_content = True
client = MyBot("bs ", intents=intents)

config = Config()
client.run(config.discord_test())
