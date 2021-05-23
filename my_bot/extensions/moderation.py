import discord
import asyncio
from discord.embeds import Embed
from discord.ext import commands
from logging import getLogger
from discord.ext.commands.core import is_owner
from discord.ext.commands import Bot
from discord.colour import Colour

log = getLogger("extensions.moderation")


class ModCog(commands.Cog, name="Moderation"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=["clear"], description="Clears the chat")
    async def cc(self, ctx, *, amount: int = 2):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                deleted = await ctx.message.channel.purge(limit=amount)
                await ctx.send(
                    f"Messages deleted by {ctx.message.author.mention}: `{len(deleted)}`"
                )
                await asyncio.sleep(1.5)
                await ctx.message.channel.purge(limit=1)
            except:
                await ctx.send("I can not delete messages here.")
        else:
            await ctx.send(embed=self._generate_no_permissions_embed())

    @commands.command(aliases=["k"], description="kicks a user from the guild")
    async def kick(self, ctx, user: discord.Member, *, reason):
        if user.guild_permissions.kick_members:
            await ctx.send(embed=self._generate_admin_not_banable_embed)
        elif ctx.message.author.guild_permissions.kick_members:
            if reason is None:
                await ctx.guild.kick(user=user, reason="None")
                await ctx.send(f"{user} has been kicked.")
            else:
                await ctx.guild.kick(user=user, reason=reason)
                await ctx.send(f"{user} has been kicked for {reason}.")
        else:
            await ctx.send(embed=self._generate_no_permissions_embed())

    @commands.command(aliases=["b"], description="bans a user from the guild")
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        if user.guild_permissions.manage_messages:
            await ctx.send(embed=self._generate_admin_not_banable_embed)
        elif ctx.message.author.guild_permissions.ban_members:
            if reason is None:
                await ctx.guild.ban(user=user, reason="None")
                await ctx.send(f"{user} has been banned.")
            else:
                await ctx.guild.ban(user=user, reason=reason)
                await ctx.send(f"{user} has been banned.")
        else:
            await ctx.send(embed=self._generate_no_permissions_embed())

    @commands.command(aliases=["ub"], description="unbans a user from the guild")
    async def unban(self, ctx, *, member):
        if ctx.mesage.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"{user.mention} got unbanned")
                    return
        else:
            await ctx.send(embed=self._generate_no_permissions_embed())

    # Error embed Section

    def _generate_no_permissions_embed(self):
        embed = discord.Embed(
            title="You do not have permissions to execute this command!",
            colour=discord.Color.dark_red()
        )
        embed.set_author(
            name="SYSTEM",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed

    def _generate_admin_not_banable_embed(self):
        embed = discord.Embed(
            title="You can't execute this command on a moderator or admin!",
            colour=discord.Color.dark_red()
        )
        embed.set_author(
            name="SYSTEM",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Info_icon_002.svg/480px-Info_icon_002.svg.png",
        )
        embed.set_thumbnail(url="https://img.icons8.com/pastel-glyph/2x/error.png")
        embed.set_footer(text=self.bot.signature)
        return embed


def setup(bot: Bot):
    bot.add_cog(ModCog(bot))
