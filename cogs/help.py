from discord.ext import commands, menus
from utils.help import PenguinHelp

import time
import aiohttp


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = PenguinHelp()
        bot.help_command.cog = self

    @commands.command(brief="Bot's latency to discord")
    async def ping(self, ctx):
        """ See bot's latency to discord """
        discord_start = time.monotonic()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com') as r:
                if r.status == 200:
                    discord_end = time.monotonic()
                    discord_ms = f"{round((discord_end - discord_start) * 1000)}ms"
                else:
                    discord_ms = "fucking dead"
                await ctx.send(f"\U0001f3d3 Pong   |   {discord_ms}")  # You can use :ping_pong: instead of \U0001f3d3


def setup(bot):
    bot.add_cog(HelpCog(bot))
