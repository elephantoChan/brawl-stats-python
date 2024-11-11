from nextcord.ext import commands


class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        """Replies with a hello message"""
        await ctx.send(f"Hello, {ctx.author.name}!")


def setup(bot):
    bot.add_cog(HelloCog(bot))
