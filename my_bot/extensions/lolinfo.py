import discord
import traceback
import requests
import json, urllib.request
from discord.ext import commands
from discord.ext.commands import Bot
from logging import getLogger
from tinydb import where

log     = getLogger("extensions.Lolinfo")

class LolInfoCog(commands.Cog, name="LeagueInfo"):
    def __init__(self, bot: Bot):
        self.bot        = bot
        self.database   = self.bot.db.table("summoner_names")
        self.API        = bot.config.api_key
        self.rankDict   = self.bot.rankDict
        self.masteryDict= self.bot.masteryDict

    @commands.command(
        aliases=["li"],
        description="Shows information about a Summoner"
    )
    async def lolinfo(self, ctx, *, summoner=None):
        version_request = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        version_json = version_request.json()
        version = version_json[0]
        if summoner is None:
            try:
                summoner = self._get_user_summoner(ctx.author.id)
            except Exception:
                traceback.print_exc()
        if summoner is not None:
            try:
                summoner_request = requests.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={self.API}')
                summoner_request.raise_for_status()
            except requests.HTTPError as exception:
                traceback.print_exc()
                await ctx.send(embed = self._generate_error_embed(summoner))
                return
            summoner_json   = summoner_request.json()
            summoner_id     = summoner_json['id']
            account_id      = summoner_json['accountId']
            puuid           = summoner_json['puuid']
            name            = summoner_json['name']
            level           = summoner_json['summonerLevel']
            icon_id         = summoner_json['profileIconId']

            icon = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{icon_id}.png'

            temp_embed = discord.Embed(description=f"Fetching {summoner}'s profile, please be patient...", color= 0xfda5b0)
            temp_embed.set_thumbnail(url= icon)
            msg = await ctx.send(embed=temp_embed)
        elif self._get_user_summoner(ctx.author.id) is None:
            await ctx.send(embed = self._generate_not_registered_embed())
            return
        else:
            await ctx.send(embed = self._generate_error_embed(summoner))

        try:
            matchhistory_request = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={self.API}')
        except Exception:
            traceback.print_exc()
        matchhistory_json = matchhistory_request.json()
        matchhistory = matchhistory_json[0:10]

        last_wins       = 0
        last_losses     = 0
        kills           = 0
        deaths          = 0
        assists         = 0
        participant_id  = None

        for m in matchhistory:
            game_id     = m
            try:
                match_request = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/{game_id}?api_key={self.API}')
            except Exception:
                traceback.print_exc()
            match_json = match_request.json()

            for pid in match_json['info']['participants']:
                try:
                    if pid['summonerId'] == summoner_id:
                        participant_id = pid['summonerId']
                except:
                    if pid['summonerId'] == account_id:
                        participant_id = pid['summonerId']

            for p in match_json['info']['participants']:
                if p['summonerId'] == participant_id:
                    kills += p['kills']
                    deaths += p['deaths']
                    assists += p['assists']
                    if p['win'] == True:
                        last_wins += 1
                    else:
                        last_losses += 1

        last_win_percentage = int((int(last_wins) / (int(last_wins) + int(last_losses))) * 100)
        average_kills       = kills / 10
        average_deaths      = deaths / 10
        average_assists     = assists / 10

        try:
            mastery_request = requests.get(f'https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={self.API}')
        except Exception:
            traceback.print_exc()
        mastery_json = mastery_request.json()

        champion_id = []
        champion_name = []
        champion_level = []
        champion_points = []

        for mastery in mastery_json[0:3]:
            champion_id.append(mastery['championId'])
            champion_level.append(mastery['championLevel'])
            champion_points.append(mastery['championPoints'])
        for cid in champion_id:
            with urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json') as f:
                champion = json.loads(f.read().decode())
            for k,v in champion['data'].items():
                if v['key'] == str(cid):
                    champion_name.append(v['name'])
            f.close()
        
        try:
            league_request = requests.get(f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={self.API}')
        except Exception:
            traceback.print_exc()
        league_json = league_request.json()
        solo_tier = ''
        solo_rank = ''
        full_solo_rank = ''
        solo_wins = '0'
        solo_losses = '0'
        solo_lp = '0'
        solo_win_ratio = '0'

        flex_tier = ''
        flex_rank = ''
        full_flex_rank = ''
        flex_wins = '0'
        flex_losses = '0'
        flex_lp = '0'
        flex_win_ratio = '0'

        solo_data = '**Unranked**'
        flex_data = '**Unranked**'

        for l in league_json:
            if l['queueType'] == 'RANKED_SOLO_5x5':
                solo_tier = l['tier']
                solo_rank = l['rank']
                solo_wins = l['wins']
                solo_losses = l['losses']
                solo_lp = l['leaguePoints']
                full_solo_rank = solo_tier + ' ' + solo_rank
                # with open('./data/ranks.json') as f:
                #     ranks = json.load(f)
                # f.close()
                solo_icon = f'{self.rankDict[solo_tier]}'
                solo_win_ratio = int((int(solo_wins) / (int(solo_wins) + int(solo_losses))) * 100)
                solo_data = f'{solo_icon} **{full_solo_rank}** \n {solo_lp} LP / {solo_wins}W {solo_losses}L \n Win Ratio {solo_win_ratio}%'

            if l['queueType'] == 'RANKED_FLEX_SR':
                flex_tier = l['tier']
                flex_rank = l['rank']
                flex_wins = l['wins']
                flex_losses = l['losses']
                flex_lp = l['leaguePoints']
                full_flex_rank = flex_tier + ' ' + flex_rank
                # with open('./data/ranks.json') as f:
                #     ranks = json.load(f)
                # f.close()
                flex_icon = f'{self.rankDict[flex_tier]}'
                flex_win_ratio = int((int(flex_wins) / (int(flex_wins) + int(flex_losses))) * 100)
                flex_data = f'{flex_icon} **{full_flex_rank}** \n {flex_lp} LP / {flex_wins}W {flex_losses}L \n Win Ratio {flex_win_ratio}%'

        embed = discord.Embed(
            title=f'Profile: {summoner}',
            description=f"Summary of the ordered Profile: \n \u200B",
            color=0xfda5b0
        )
        embed.set_thumbnail(url= icon)
        embed.add_field(
            name='Summoner Level', value=f'{level} \n \u200B'
        )
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(
            name='Ranked (Solo/Duo)',
            value=f'{solo_data} \n \u200B'
        )
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(
            name='Ranked (Flex)',
            value=f'{flex_data} \n \u200B'
        )
        embed.add_field(
            name='Recent 10 Games', 
            value=f'{average_kills} K / {average_deaths} D / {average_assists} A \n {last_wins}W {last_losses}L \n Win Ratio {last_win_percentage}% \n \u200B'
        )
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(
            name='Highest Champion Mastery', 
            value=f'''
                        [{self.masteryDict[str(champion_level[0])]}] {champion_name[0]}: {champion_points[0]:,}
                        [{self.masteryDict[str(champion_level[1])]}] {champion_name[1]}: {champion_points[1]:,}
                        [{self.masteryDict[str(champion_level[2])]}] {champion_name[2]}: {champion_points[2]:,}
                        \u200B'''
        )
        await msg.edit(embed=embed)

    def _get_user_summoner(self, user_id):
        results = self.database.search(where("user") == user_id)
        if len(results) > 0:
            return results[0]["summoner"]
        else:
            return None

    # Error Embeds

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

    def _generate_error_embed(self, summoner_name):
        embed = discord.Embed(
            title="Summoner: " + summoner_name + " could not be found!",
            description="Please check your input",
            color=0x102319,
        )
        embed.add_field(
            name='Usage',
            value='.lolinfo <Summoner>'
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