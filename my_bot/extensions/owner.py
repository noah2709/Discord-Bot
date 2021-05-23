from discord.embeds import Embed
from discord.ext import commands
from logging import getLogger
from discord.ext.commands.core import is_owner
from discord.ext.commands import Bot
from discord.colour import Colour

log = getLogger("extensions.owner")


class OwnerCog(commands.Cog, name="Owner"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(
        aliases=["r"], 
        description="restart the bot"
    )
    @is_owner()
    async def restart(self, ctx):
        embed = Embed(
            title="Restarting...",
            colour=Colour.dark_gold(),
        )
        embed.set_author(name="SYSTEM")
        embed.set_footer(text=self.bot.signature)
        await ctx.send(embed=embed)
        exit(104)

    @commands.command(
        aliases=["re"],
        description="reload one extension"
        )
    @is_owner()
    async def reload(self, ctx, name: str):
        try:
            self.bot.reload_extension(f"extensions.{name}")
        except Exception as e:
            return await log.error(f"Couldn't reload Extension: {name}")
        await ctx.send(embed=self._generate_reload_embed(name))
        log.info(f"Reloaded Extension: {name}")

    def _generate_reload_embed(self, name):
        embed = Embed(
            title=f"Extension: {name}, successfully reloaded",
            colour=Colour.dark_gold(),
        )
        embed.set_author(
            name="SYSTEM",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png"
        )
        embed.set_footer(text=self.bot.signature)
        return embed

def setup(bot: Bot):
    bot.add_cog(OwnerCog(bot))