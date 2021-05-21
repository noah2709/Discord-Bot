import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from logging import getLogger
from requests import HTTPError
from discord.colour import Colour
from tinydb import where

log = getLogger("extensions.lollogout")


class LolLogoutCog(commands.Cog, name="LeagueLogout"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.summoner = self.bot.db.table("summoner_names")

    @commands.command(
        aliases=["llo"], 
        description="Deletes your Summoner Name"
    )
    async def lollogout(self, ctx: Context):
        if self._is_user_registered(ctx.author.id) == True:
            self.summoner.remove(where("user") == ctx.author.id)
            await ctx.send(embed=self._generate_user_deleted_embed())
        else:
            await ctx.send(embed=self._generate_error_embed())

    def _is_user_registered(self, user_id):
        return len(self.summoner.search(where("user") == user_id)) > 0
    
    def _generate_user_deleted_embed(self):
        embed = discord.Embed(
            title="Successfully deleted your user",
            description="You can register a new one now", 
            colour=Colour.dark_orange()
        )
        embed.set_author(
            name="LOLLOGOUT",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_error_embed(self):
        embed = discord.Embed(
            title="You can't logout if you're not registered!",
            description="You can register with .lollogin <Summoner>", 
            colour=Colour.dark_red()
        )
        embed.set_author(
            name="LOLLOGOUT",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed

def setup(bot):
    bot.add_cog(LolLogoutCog(bot))