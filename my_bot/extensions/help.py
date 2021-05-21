from os import name
import discord
from discord import colour
from discord.ext import commands
from discord.ext.commands import Bot
from discord.colour import Color
from logging import getLogger


log = getLogger("extensions.help")


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help",
            description="Use .help <command> for extended information",
            colour=Color.dark_blue(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(
            name="Moderation",
            value="kick, ban, unban, clearchat",
            inline=False,
        )
        embed.add_field(
            name="Misc",
            value="ping, MagicConch",
            inline=False,
        )
        embed.add_field(
            name="League of Legends",
            value="LeagueInfo, LeagueLogin, LeagueLogout", 
            inline=False,
        )
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    # Moderation Section

    @help.command()
    async def kick(self, ctx):

        embed = discord.Embed(
            title="Kick Command",
            description="Kicks a member from the Server",
            colour=Color.dark_green(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".kick <member> [reason]")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx):

        embed = discord.Embed(
            title="Ban Command",
            description="Kicks a member from the Server",
            colour=Color.dark_green(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".ban <member> [reason]")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    @help.command()
    async def unban(self, ctx):

        embed = discord.Embed(
            title="Unban Command",
            description="Unbans a banned user",
            colour=Color.dark_green(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".unban <member>")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    @help.command()
    async def clearchat(self, ctx):

        embed = discord.Embed(
            title="Clear Chat Command",
            description="Clears the Chat",
            colour=Color.dark_green(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".cc [value]")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    # Misc Section

    @help.command()
    async def ping(self, ctx):

        embed = discord.Embed(
            title="Ping",
            description="Checks your latency to the bot",
            colour=Color.dark_magenta(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".ping")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    @help.command()
    async def MagicConch(self, ctx):

        embed = discord.Embed(
            title="The Magic Conch",
            description="The Spongebob Magic Conch (8Ball)",
            colour=Color.dark_magenta(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".mcs [question]")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    # LoL Section

    @help.command()
    async def LeagueInfo(self, ctx):

        embed = discord.Embed(
            title="League Info Command",
            description="Shows information about a Summoner",
            colour=Color.dark_orange(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".lolinfo <Summoner Name>")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)
    
    @help.command()
    async def LeagueLogin(self, ctx):

        embed = discord.Embed(
            title="League Login Command",
            description="Saves your Summoner name so you can type .lolinfo <me> to find yourself",
            colour=Color.dark_orange(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".lollogin <Summoner Name>")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)

    @help.command()
    async def LeagueLogout(self, ctx):

        embed = discord.Embed(
            title="League Logout Command",
            description="Unsaves your Summoner name so you can register a new one",
            colour=Color.dark_orange(),
        )
        embed.set_author(
            name="HELPER",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.add_field(name="**Syntax**", value=".lollogout")
        embed.set_footer(text=self.bot.signature)

        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(HelpCog(bot))
