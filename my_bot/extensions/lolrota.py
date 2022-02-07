import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from logging import getLogger
from riotwatcher import LolWatcher
from leaguenames import leaguenames
import datetime
from datetime import date

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
        from_now    = date.today().strftime("%d %B, %Y")
        until_temp  = datetime.datetime.now() + datetime.timedelta(days=7)
        until       = until_temp.strftime("%d %B, %Y")

        durationString = f"{from_now} - {until}"

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
        clearnames = []
        championString1 = ''
        championString2 = ''
        for freechampid in freechampids:
            clearname = leaguenames(freechampid)
            clearnames.append(clearname)
        
        for champ in clearnames:
            if len(championString1) <= 1000:
                championString1 += f'{self.champDict[champ]} **{champ}**\n'
            else:
                championString2 += f'{self.champDict[champ]} **{champ}**\n'
        self.shown_rota.insert({"freeChampionIds": freechampids})
    

        durationString = f'`{durationString}`'

        embed1 = discord.Embed(
            title='Current Free Champion Rotation',
            color=0x109319
        )
        embed1.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png'
        )
        embed1.add_field(
            name='Duration',
            value=durationString,
            inline=False
        )
        embed1.add_field(
            name='Champions',
            value=championString1,
            inline=False
        )

        if len(championString2) != 0:

            embed2 = discord.Embed(
                title='Current Free Champion Rotation',
                color=0x109319
            )
            embed2.set_thumbnail(
                url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/256px-LoL_icon.svg.png'
            )
            embed2.add_field(
                name='Duration',
                value=durationString,
                inline=False
            )
            embed2.add_field(
                name='Champions',
                value=championString2,
                inline=False
            )
            return embed1, embed2
        
        else:
            return embed1


    @lolrota.before_loop
    async def before_lolrota(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(LolRotaCog(bot))