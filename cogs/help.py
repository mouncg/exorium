from discord.ext import commands, menus
from utils.help import PenguinHelp

import discord
import config
import time
import aiohttp


class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = PenguinHelp()
        bot.help_command.cog = self

    @commands.command()
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


    @commands.command()
    async def invite(self, ctx):
        """ Invite Esquire to your server """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"Invite Esquire to your server [here]({config.invite})."
        await ctx.send(embed=e)


    @commands.command()
    async def privacy(self, ctx):
        """ Read our privacy policy """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"Read Esquire's privacy policy [here]({config.privacy})."
        await ctx.send(embed=e)


    @commands.command()
    async def support(self, ctx):
        """ Get support with Esquire """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"""
You can get support here:
- [support server]({config.support})
- [Github issue](https://github.com/ThePawKingdom/exorium/issues/new)
"""
        await ctx.send(embed=e)
                        


def setup(bot):
    bot.add_cog(HelpCog(bot))
