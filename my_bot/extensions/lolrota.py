import discord
from discord.ext import commands, tasks
from logging import getLogger
from riotwatcher import LolWatcher
from discord.ext.commands import Bot
from leaguenames import leaguenames
from datetime import date

log = getLogger("extensions.lolrota")


class LolRotaCog(commands.Cog, name="LeagueRota"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.shown_rota = self.bot.db.table("shown_rota")

        self.today = date.today().strftime("%d.%m.%Y")

        self.watcher = LolWatcher(bot.config.api_key)
        self.lolrota.start()

    @tasks.loop(minutes=30)
    async def lolrota(self):
        # Get the rota
        fetch = self.watcher.champion.rotations("euw1")
        freechampids = fetch["freeChampionIds"]
        # Check if the rota is new
        shown_rota = [elem["freeChampionIds"] for elem in self.shown_rota.all()]
        ListEmpty = False
        # if shown_rota[-1] == freechampids:
        #     pass
        if not shown_rota:
            self.shown_rota.insert({"freeChampionIds": freechampids})
            # Get the Clearnames
            clearnames = []
            for freechampid in freechampids:
                clearname = leaguenames(freechampid)
                clearnames.append(f"- {clearname}\n")
            # Create the Embed
            embed = discord.Embed(
                title=f"Champion Rotation {self.today}",
                description="Here you get the Champion rotation every week",
                colour=discord.Colour.blurple(),
            )
            embed.set_author(
                name="LOLROTA",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
            )
            embed.add_field(
                name="Free Champions",
                value="".join(clearnames),
            )
            embed.set_footer(text=self.bot.signature)
            channel = self.bot.get_channel(int(self.bot.config.rota_channel_id))
            await channel.send(embed=embed)
        elif shown_rota[-1] != freechampids:
            self.shown_rota.insert({"freeChampionIds": freechampids})
            # Get the Clearnames
            clearnames = []
            for freechampid in freechampids:
                clearname = leaguenames(freechampid)
                clearnames.append(f"- {clearname}\n")
            # Create the Embed
            embed = discord.Embed(
                title=f"Champion Rotation {self.today}",
                description="Here you get the Champion rotation every week",
                colour=discord.Colour.blurple(),
            )
            embed.set_author(
                name="LOLROTA",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png",
            )
            embed.add_field(
                name="Free Champions",
                value="".join(clearnames),
            )
            embed.set_footer(text=self.bot.signature)
            channel = self.bot.get_channel(int(self.bot.config.rota_channel_id))
            await channel.send(embed=embed)
        else:
            pass

    @lolrota.before_loop
    async def before_lolrota(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(LolRotaCog(bot))
