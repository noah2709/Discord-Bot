import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from logging import getLogger
from bs4 import BeautifulSoup
import requests
from riotwatcher import LolWatcher
from leaguenames import leaguenames

log = getLogger("extensions.lolrota")
URL = 'https://leagueoflegends.fandom.com/wiki/Free_champion_rotation#Classic'

class LolRotaCog(commands.Cog, name="LeagueRota"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.champDict = self.bot.champDict
        self.shown_rota = self.bot.db.table("shown_rota")

        self.watcher = LolWatcher(bot.config.api_key)
        self.lolrota.start()

    @tasks.loop(hours=4)
    async def lolrota(self):
        result          = requests.get(URL)
        soup            = BeautifulSoup(result.content, 'html.parser')
        durationString  = soup.find('div', attrs={'id':'rotationweek'}).text

        fetch = self.watcher.champion.rotations("euw1")
        freechampids = fetch["freeChampionIds"]

        shown_rota = [elem["freeChampionIds"] for elem in self.shown_rota.all()]

        channel = self.bot.get_channel(int(self.bot.config.rota_channel_id))

        if not shown_rota:
            await channel.send(embed=self._generate_rota_embed(durationString, freechampids))
        elif shown_rota[-1] != freechampids:
            await channel.send(embed=self._generate_rota_embed(durationString, freechampids))
        else:
            pass

    def _generate_rota_embed(self, durationString, freechampids):
        self.shown_rota.insert({"freeChampionIds": freechampids})
        clearnames = []
        championString = ''
        for freechampid in freechampids:
            clearname = leaguenames(freechampid)
            clearnames.append(clearname)
        for champ in clearnames:
            championString += f'{self.champDict[champ]} **{champ}**\n'

        durationString = f'`{durationString}`'

        embed = discord.Embed(
            title='Current Free Champion Rotation',
            color=0x109319
        )
        embed.set_thumbnail(
            url='https://static.wikia.nocookie.net/leagueoflegends/images/e/e6/Site-logo.png/revision/latest?cb=20210601132313'
        )
        embed.add_field(
            name='Duration',
            value=durationString,
            inline=False
        )
        embed.add_field(
            name='Champions',
            value=championString,
            inline=False
        )
        return embed

    @lolrota.before_loop
    async def before_lolrota(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(LolRotaCog(bot))