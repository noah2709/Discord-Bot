import discord
import requests
import re
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from logging import getLogger

log     = getLogger("extensions.patchnotes")

class PatchnotesCog(commands.Cog, name="Patchnotes"):
    def __init__(self, bot: Bot):
        self.bot        = bot
        self.shown_patch= self.bot.db.table("shown_patch")

        self.patch.start()

    @tasks.loop(hours=12)
    async def patch(self):
        patch_request   = requests.get("https://www.leagueoflegends.com/en-us/news/tags/patch-notes/")
        soup            = BeautifulSoup(patch_request.content, 'html.parser')
        patch           = soup.find('div', attrs={'class':'style__InfoInner-sc-1h41bzo-7 djDzKv'}).h2.text

        channel = self.bot.get_channel(int(self.bot.config.patch_notes_channel_id))

        shown_patch = [elem["Patch"] for elem in self.shown_patch.all()]

        if not shown_patch:
            await channel.send(embed=self._generate_patch_post(patch))
        if shown_patch[-1] != patch:
            await channel.send(embed=self._generate_patch_post(patch))
        else:
            pass

    def _generate_patch_post(self, patch):
        self.shown_patch.insert({"Patch": patch})
        current_patch = re.sub('[^0-9.]', '', patch).replace('.', '-')
        current_patch_link = f"https://www.leagueoflegends.com/en-us/news/game-updates/patch-{current_patch}-notes/"
        patch_data_request = requests.get(current_patch_link)
        data_soup = BeautifulSoup(patch_data_request.content, 'html.parser')
        patch_text= data_soup.find('blockquote', attrs={'class':'blockquote context'}).text
        patch_image= data_soup.find('a', attrs={'class':'skins cboxElement'}).img['src']

        embed = discord.Embed(
            title=f'[{patch}]',
            url=current_patch_link,
            color=0x109319
        )
        embed.add_field(
            name='**Patch Text**',
            value=patch_text,
            inline=False
        )
        embed.set_image(
            url=patch_image
        )
        return embed

    @patch.before_loop
    async def before_patch(self):
        await self.bot.wait_until_ready()
        
def setup(bot):
    bot.add_cog(PatchnotesCog(bot))