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
        embed.set_author(
            name="SYSTEM",
            icon_url=ctx.guild.icon_url
            )
        embed.set_footer(text=self.bot.signature)
        await ctx.send(embed=embed)
        exit(104)

    @commands.command(
        aliases=["gp"], 
        description="updates the bot"
    )
    @is_owner()
    async def gitpull(self, ctx):
        embed = Embed(
            title="Getting Data... / Restarting...",
            colour=Colour.dark_gold(),
        )
        embed.set_author(
            name="SYSTEM",
            icon_url=ctx.guild.icon_url
            )
        embed.set_footer(text=self.bot.signature)
        await ctx.send(embed=embed)
        exit(187)

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
        await ctx.send(embed=self._generate_reload_embed(ctx, name))
        log.info(f"Reloaded Extension: {name}")

    def _generate_reload_embed(self, ctx, name): 
        embed = Embed(
            title=f"Extension: {name}, successfully reloaded",
            colour=Colour.dark_gold(),
        )
        embed.set_author(
            name="SYSTEM",
            icon_url=ctx.guild.icon_url
        )
        embed.set_footer(text=self.bot.signature)
        return embed

def setup(bot: Bot):
    bot.add_cog(OwnerCog(bot))