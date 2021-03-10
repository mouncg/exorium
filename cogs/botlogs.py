import discord, config, time, aiohttp, psutil, platform
from collections import Counter
from discord.ext import commands
from datetime import datetime
from utils import default

class botlogs(commands.Cog, name="Bot logs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log = self.bot.get_channel(755138117488345118)
        
        e = discord.Embed(color=config.color)
        e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        e.description = f"""
**Message content:**
{ctx.message.clean_content}

**Author ID:** [{ctx.author.id}](https://discord.com/users/{ctx.author.id})

**Guild:** {ctx.guild.name} (`{ctx.guild.id}`) 
"""
        e.set_footer(text=datetime.now().__format__('%a %d %b %y, %H:%M'))
        e.set_thumbnail(url=ctx.guild.icon_url)
        await log.send(embed=e)

def setup(bot):
    bot.add_cog(botlogs(bot))
