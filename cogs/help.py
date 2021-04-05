from discord.ext import commands, menus
from utils.help import PenguinHelp
from collections import Counter

import discord
import config
import time
import aiohttp
import psutil
import platform


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


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """ Make suggestions for Esquire """
        channel = self.bot.get_channel(822611562119692304)
        if len(suggestion) >= 500:
            return await ctx.send(f"Please make your suggestion shorter then 500 characters.")
        e = discord.Embed(color=discord.Color.green())
        e.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
        e.description = suggestion
        ra = await channel.send(embed=e)
        await ra.add_reaction(config.checkmark)
        await ra.add_reaction(config.crossmark)
        await ctx.send(f"Your suggestion was recorded in our support server.")


    @commands.command()
    @commands.guild_only()
    async def id(self, ctx, member: discord.Member):
        """ Get a user's ID """
        await ctx.reply(member.id)


    @commands.command()
    async def av(self, ctx, member: discord.Member):
        """ Get a user's avatar """
        if not member:
            member = ctx.author

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_image(url=member.avatar_url)
        e.set_footer(text=f"avatar: {member}")
        await ctx.send(embed=e)


    @commands.command()
    @commands.guild_only()
    async def servericon(self, ctx):
        """ Get the server's icon """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)


    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(add_reactions=True)
    async def poll(self, ctx, *, poll):
        """ Host a poll """
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        e = discord.Embed(color=discord.Color.green())
        e.description = poll
        e.set_footer(text=f"Host: {ctx.author}")
        pre = await ctx.send(embed=e)
        await pre.add_reaction(config.checkmark)
        await pre.add_reaction(config.crossmark)


    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, *, say):
        """ Say something with Esquire """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = say
        e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


    @commands.command(aliases=["statistics"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx):
        """ See Esquire's statistics """

        chtypes = Counter(type(c) for c in self.bot.get_all_channels())
        voice = chtypes[discord.channel.VoiceChannel]
        text = chtypes[discord.channel.TextChannel]

        cpup = psutil.cpu_percent()
        core = psutil.cpu_count()
        mem = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20
        storage_free = psutil.disk_usage('/').free >> 30

        Joshua = await self.bot.fetch_user(809057677716094997)
        Moksej = await self.bot.fetch_user(345457928972533773)
        Duck = await self.bot.fetch_user(443217277580738571)
        Tooth = await self.bot.fetch_user(341988909363757057)

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_thumbnail(url=self.bot.user.avatar_url)

        humans = len(ctx.guild.humans)
        bots = len(ctx.guild.bots)

        e.description = f"""
__**About**__
Developers:
- **{str(Joshua)}** & **{str(Moksej)}**
- **{str(Duck)}** & **{str(Tooth)}**

Library: [enhanced dpy {discord.__version__}](https://github.com/iDutchy/discord.py)

__**Statistics**__
**{len(self.bot.guilds)}** Guilds
**N/A** Users (**N/A** humans & **N/A** bots)
**{text}** text & **{voice}** voice channels

__**System**__
Hosted on **{platform.platform()}**
**{core}** cores
**{cpup}**% CPU load
**{mem_usage}**/**{mem}** MB memory used
**{storage_free}** MB storage free 
"""

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(HelpCog(bot))