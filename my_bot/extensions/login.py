import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from logging import getLogger
from requests import HTTPError
from discord.colour import Colour
from riotwatcher import LolWatcher
from tinydb import where

log = getLogger("extensions.lollogin")


class LolLoginCog(commands.Cog, name="LeagueLogin"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.summoner = self.bot.db.table("summoner_names")
        self.watcher = LolWatcher(bot.config.api_key)

    @commands.command(aliases=["ll"], description="Saves your Summoner-Name")
    async def lollogin(self, ctx: Context, *, name):
        if self._is_user_registered(ctx.author.id):
            await ctx.send(embed=self._generate_error_embed())
            return

        if self._summoner_exists(name) == True:
            self.summoner.insert({"user": ctx.author.id, "summoner": name})
            await ctx.send(embed=self._generate_success_embed(name))
        else:
            await ctx.send(embed=self._generate_summoner_not_found_embed(name))

    def _is_user_registered(self, user_id):
        return len(self.summoner.search(where("user") == user_id)) > 0

    def _generate_error_embed(self):
        embed = discord.Embed(
            title="You're already registered", colour=Colour.dark_red()
        )
        embed.set_author(
            name="LOLLOGIN",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_success_embed(self, summoner_name):
        embed = discord.Embed(
            title=f"Successfully added {summoner_name} to your Account",
            colour=Colour.blurple(),
        )
        embed.add_field(name="Get your stats here", value=".lolinfo me")
        embed.set_author(
            name="LOLLOGIN",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_summoner_not_found_embed(self, summoner_name):
        embed = discord.Embed(
            title=f"Summoner: {summoner_name}, could not be found!",
            colour=Colour.dark_red(),
        )
        embed.set_author(
            name="LOLLOGIN",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed

    def _summoner_exists(self, summoner_name):
        try:
            self.watcher.summoner.by_name("euw1", summoner_name)
            return True
        except HTTPError:
            return False


def setup(bot):
    bot.add_cog(LolLoginCog(bot))
