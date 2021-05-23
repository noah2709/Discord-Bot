import discord
from discord.ext import commands
from logging import getLogger
from requests.models import HTTPError
from riotwatcher import LolWatcher
from requests import HTTPError
from discord.ext.commands import Bot
from tinydb import where

log = getLogger("extensions.lolinfo")


class LolInfoCog(commands.Cog, name="LeagueInfo"):
    def __init__(self, bot: Bot):
        self.watcher = LolWatcher(bot.config.api_key)
        self.bot = bot
        self.summoner = self.bot.db.table("summoner_names")

    @commands.command(
        aliases=["li"], 
        description="Shows information about a Summoner"
    )
    async def lolinfo(self, ctx, *, name):
        if name == "me":
            name = self._get_user_summoner(ctx.author.id)

        if name is None:
            await ctx.send(embed=self._generate_not_registered_embed())
            return

        try:
            summoner = self.watcher.summoner.by_name("euw1", name)
            stats = self.watcher._league.by_summoner("euw1", summoner["id"])
            if self._is_unranked(stats) == True:
                await ctx.send(embed=self._generate_summoner_found_unranked_embed(summoner))
            else:
                await ctx.send(embed=self._generate_summoner_found_ranked_embed(summoner, stats))
        except HTTPError:
            await ctx.send(embed=self._generate_error_embed(name))

    def _is_unranked(self, stats):
        if len(stats) == 0:
            return True
        else:
            return False

    def _get_user_summoner(self, user_id):
        results = self.summoner.search(where("user") == user_id)
        if len(results) > 0:
            return results[0]["summoner"]
        else:
            return None

    def _generate_summoner_found_unranked_embed(self, summoner):
        lvl = summoner["summonerLevel"]
        icon = summoner["profileIconId"]
        
        embed = discord.Embed(
            title="Summoner: " + summoner["name"],
            description="Here you get all Information you'll need",
            colour=discord.Colour.blurple(),
        )
        embed.set_author(
            name="LOLINFO",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(
            url="https://ddragon.leagueoflegends.com/cdn/9.3.1/img/profileicon/"
            + str(icon)
            + ".png"
        )
        embed.add_field(name="Elo:", value="UNRANKED", inline=False)
        embed.add_field(name="Account Level", value="Level: " + str(lvl))
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_not_registered_embed(self):
        embed = discord.Embed(
            title="First you need to register yourself!",
            description="Use the command .lollogin <Summoner> to register yourself",
            colour=discord.Color.dark_red(),
        )
        embed.set_author(
            name="LOLINFO",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_summoner_found_ranked_embed(self, summoner, stats):
        tier = stats[0]["tier"]
        rank = stats[0]["rank"]
        lp = stats[0]["leaguePoints"]
        lvl = summoner["summonerLevel"]
        icon = summoner["profileIconId"]
        wins = int(stats[0]["wins"])
        losses = int(stats[0]["losses"])
        winrate = int((wins / (wins + losses)) * 100)
        
        embed = discord.Embed(
            title=f"Summoner: " + summoner["name"],
            description="Here you get all Information you'll need",
            color=0x109319,
        )
        embed.set_author(
            name="LOLINFO",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(
            url="https://ddragon.leagueoflegends.com/cdn/9.3.1/img/profileicon/"
            + str(icon)
            + ".png"
        )
        embed.add_field(
            name=f"Elo:", value=str(tier) + " " + str(rank), inline=False
        )
        embed.add_field(
            name="More Information",
            value=f"WR: " + str(winrate) + "% " + " LP: " + str(lp),
            inline=True,
        )
        embed.add_field(
            name="Account Level", value="Level: " + str(lvl), inline=True
        )
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_error_embed(self, summoner_name):
        embed = discord.Embed(
            title="Summoner: " + summoner_name + " could not be found!",
            description="Please check your input",
            color=0x102319,
        )
        embed.set_author(
            name="LOLINFO",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed

def setup(bot):
    bot.add_cog(LolInfoCog(bot))
