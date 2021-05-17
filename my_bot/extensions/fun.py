from discord.ext import commands
from discord.ext.commands import Bot
from logging import getLogger
import random

log = getLogger('extensions.fun')

class FunCog(commands.Cog, name="Fun"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def mcs(self, ctx, *, question):
        responses = [
            "Gar nichts.",
            "Keins von beidem.",
            "Ich glaub eher nicht.",
            "Eines Tages vielleicht.",
            "Nein!",
            "Nein :(",
            "Ja.",
            "Frag doch einfach nochmal.",
        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


def setup(bot):
    bot.add_cog(FunCog(bot))
