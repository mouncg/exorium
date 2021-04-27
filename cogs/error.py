import asyncio
import discord
import traceback
from discord.ext import commands


class error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

        if isinstance(error, commands.CommandOnCooldown):
            cd = discord.Embed(color=discord.Color.red())
            e.description = f"This command is in cooldown."
            return await ctx.send(embed=cd)

def setup(bot):
    bot.add_cog(error(bot))
