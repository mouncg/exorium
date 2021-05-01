import asyncio
import discord
import traceback
import config
from discord.ext import commands
from utils.checks import admin_only


class error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_perms) + "`"
            return await ctx.send(f"{config.crossmark} **You are missing {perms} permissions.**")

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_perms) + "`"
            return await ctx.send(f"{config.crossmark} **I'm missing {perms} permissions**")

        if isinstance(err, admin_only):
            await ctx.send(f"{config.crossmark} **Only __bot admins__ can use this command.**")

        if isinstance(err, commands.MissingRequiredArgument):
            return await ctx.send(f"**You are missing required arguments - {err.param}**")

        if isinstance(err, commands.CommandOnCooldown):
            clog = await self.bot.fetch_channel(837690526789533697)
            e = discord.Embed(color=discord.Color.red())
            e.description = f"**{ctx.author} has a `{err.retry_after:.0f}` second cooldown on command `{ctx.command.qualified_name}`**" \
                            f"\nGuild **{ctx.guild}** with ID `{ctx.guild.id}` | User ID: `{ctx.author.id}`"
            await clog.send(embed=e)
            return await ctx.send(f"`{ctx.command.qualified_name}` **is on cooldown for __{err.retry_after:.0f}__ more seconds.**")

        if isinstance(err, commands.NotOwner):
            return await ctx.send(f"{config.crossmark} **Only __bot owners__ can use this command.**")

        if isinstance(err, commands.MemberNotFound):
            return await ctx.send(f"{config.confused} **Could not find user `{err.argument}`**")

        if isinstance(err, commands.ChannelNotFound):
            return await ctx.send(f"{config.confused} **Could not find channel `{err.argument}`**")

        if isinstance(err, commands.MessageNotFound):
            return await ctx.send(f"{config.confused} **Could not find message `{err.argument}`**")


        else:
            e = discord.Embed(title="traceback", color=discord.Color.red())
            e.description = f"**Full traceback**\n```py\n{''.join(traceback.format_exception(type(err), err, err.__traceback__))}\n```"
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(error(bot))
