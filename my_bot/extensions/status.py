from itertools import cycle
from logging import getLogger
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
import discord

log = getLogger('extensions.Cycle')
status = cycle(['"Type .help for help"', 'Developed by Taikador'])

class CycleCog(commands.Cog, name="Cycle"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.change_status.start()

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(status)))
    
    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()
        
def setup(bot):
    bot.add_cog(CycleCog(bot))