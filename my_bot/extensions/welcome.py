import discord
from discord.ext import commands
import datetime

from discord.ext.commands.bot import Bot
from discord.member import Member


class WelcomeCog(commands.Cog, name="Welcome"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        embed = discord.Embed(
            title=f"Welcome {member}",
            colour=discord.Colour(0xC11AA2),
            description="If you have any questions, feel free to ask.",
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_thumbnail(url=member.guild.banner_url)
        embed.set_author(
            name=member.name,
            icon_url=member.avatar_url,
        )
        embed.set_footer(
            text=member.guild,
            icon_url=member.guild.icon_url,
        )
        channel = member.guild.get_channel(int(self.bot.config.welcome_channel_id))
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(WelcomeCog(bot))
