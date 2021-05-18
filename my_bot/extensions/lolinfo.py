import discord
from discord.ext import commands
from logging import getLogger
from requests.models import HTTPError
from riotwatcher import LolWatcher
from requests import HTTPError
from discord.ext.commands import Bot

log = getLogger('extensions.lol')

class LolInfoCog(commands.Cog, name="LeagueInfo"):
    def __init__(self, bot: Bot):
        self.watcher = LolWatcher(bot.config.api_key)
        self.bot = bot

    @commands.command()
    async def lolinfo(self, ctx, *, name):
        try:
            summoner = self.watcher.summoner.by_name("euw1", name)
            stats = self.watcher._league.by_summoner("euw1", summoner["id"])
            if len(stats) == 0:
                summoner = self.watcher.summoner.by_name("euw1", name)
                stats = self.watcher._league.by_summoner("euw1", summoner["id"])
                lvl = summoner["summonerLevel"]
                icon = summoner["profileIconId"]

                embed = discord.Embed(
                    title="Summoner: " + summoner["name"],
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
                embed.add_field(name="Elo:", value="UNRANKED", inline=False)
                embed.add_field(name="Account Level", value="Level: " + str(lvl))
                embed.set_footer(text="League of Legends | All Rights reserved")
                await ctx.send(embed=embed)
                pass
            else:
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
                await ctx.send(embed=embed)
                pass
        except HTTPError:
            summoner = name
            embed = discord.Embed(
                title="Summoner: " + summoner + " could not be found!",
                description="Please check your input",
                color=0x102319,
            )
            embed.set_author(
                name="LOLINFO",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
            )
            embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
            embed.set_footer(text=self.bot.signature)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LolInfoCog(bot))
