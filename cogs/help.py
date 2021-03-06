import discord
import config
import time
import aiohttp
import psutil
import platform

from discord.ext import commands, menus
from utils.help import PenguinHelp
from utils import default
from collections import Counter


class HelpCog(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = PenguinHelp()
        bot.help_command.cog = self
        self.help_icon = '<:discovery:719431405905379358>'

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
        channel = self.bot.get_channel(769132481252818954)
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
    async def av(self, ctx, user: discord.Member = None):
        """ Get a user's avatar """
        if not user:
            user = ctx.message.author

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_image(url=user.avatar_url)
        e.set_footer(text=f"avatar: {user}")
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """" Get information about the server """

        owner = await self.bot.fetch_user(ctx.guild.owner_id)
        member_count = ctx.guild.member_count  # last known count because you don't have intents
        features = ", ".join(ctx.guild.features).lower().replace('_', ' ').title() if len(ctx.guild.features) != 0 else None
        mfa = "Optional" if ctx.guild.mfa_level else "Required"
        verification = str(ctx.guild.verification_level).capitalize()

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_author(name=f"{ctx.guild.name} Information", icon_url=ctx.guild.icon_url)
        e.add_field(name="**General Information**",
                    value=f"**Owner:** {owner} ({owner.id})\n**Guild Created At:** {default.date(ctx.guild.created_at)}\n"
                          f"**Guild Region:** {ctx.guild.region}\n**MFA:** {mfa}\n**Verification Level:** {verification}")
        e.add_field(name="**Other**",
                    value=f"**Avg Member Count:** {member_count:,}\n**Text Channels:** {len(ctx.guild.text_channels)}\n"
                          f"**Voice Channels:** {len(ctx.guild.voice_channels)}")
        if features:
            e.add_field(name="**Server Features**",
                        value=features,
                        inline=False)

        if not ctx.guild.is_icon_animated():
            e.set_thumbnail(url=ctx.guild.icon_url_as(format="png"))
        elif ctx.guild.is_icon_animated():
            e.set_thumbnail(url=ctx.guild.icon_url_as(format="gif"))
        if ctx.guild.banner:
            e.set_image(url=ctx.guild.banner_url_as(format="png"))
        e.set_footer(text=f"Guild ID: {ctx.guild.id}")
        await ctx.send(embed=e)

    @commands.command(aliases=["ui"])
    @commands.guild_only()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """ See a user's info """
        if not user:
            user = ctx.author

        if str(user.status) == 'dnd':
            status = 'Do Not Disturb'
        else:
            status = user.status

        uroles = []
        for role in user.roles:
            if role.is_default():
                continue
            uroles.append(role.mention)

        uroles.reverse()

        if len(uroles) > 10:
            uroles = [f"{', '.join(uroles[:10])} (+{len(user.roles) - 11})"]

        e = discord.Embed(color=user.colour)
        e.set_author(name=user.display_name, icon_url=user.avatar_url)
        e.set_thumbnail(url=user.avatar_url)
        e.description = f"""
**Username:** {user}
**User ID:** {user.id}
**Created on {default.date(user.created_at)}**
**Joined on {default.date(user.joined_at)}**
**Flag value:** {user.public_flags.value}
**Status:** {status}
"""
        if len(uroles) > 0:
            e.add_field(name=f"__**Roles ({len(user.roles) - 1})**__",
                        value=", ".join(uroles), inline=False)

        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        """ See a role's info """

        managed = "Yes" if role.managed else "No"
        hoisted = "Yes" if role.hoist else "No"
        position = len(ctx.guild.roles) - role.position
        permissions = dict(role.permissions)
        perms = []
        for perm in permissions.keys():
            if permissions[
                perm] is True and not role.permissions.administrator:  # I guess role.permissions.administrator works, not sure
                perms.append(perm.lower().replace('_', ' ').title())

        if role.permissions.administrator:
            perms.append("Administrator")

        rolemembers = []
        for member in role.members:
            rolemembers.append(member.mention)

        if len(rolemembers) > 10:
            rolemembers = [f"{', '.join(rolemembers[:10])} (+{len(role.members) - 11})"]

        e = discord.Embed(color=role.color)
        e.description = f"""
**ID:** {role.id}
**Created at:** {default.date(role.created_at)}
**Managed:** {managed}
**Position:** {position}
**Hoisted:** {hoisted}
**Color:** `{role.colour}`
**Permissions:** `{"`, `".join(perms)}`
**Members ({len(role.members)}):** {", ".join(rolemembers)} 
"""
        await ctx.send(f"Information about role **{role.name}**", embed=e)

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

        devs = [f"{x.name}#{x.discriminator}" for x in
                self.bot.get_guild(755068089233834074).get_role(828339695314403378).members]
        dev1 = ', '.join(devs)

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_thumbnail(url=self.bot.user.avatar_url)

        humans = len(ctx.guild.humans)
        bots = len(ctx.guild.bots)

        e.description = f"""
__**About**__
Developers:
- **[{Joshua}](https://discordrep.com/u/809057677716094997#)**
- **[{Moksej}](https://discordrep.com/u/345457928972533773#)**
- **[{Duck}](https://discordrep.com/u/443217277580738571#)**

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


    @commands.group(aliases=["emoji"])
    async def emote(self, ctx):
        """ Get emote info/url """
        if ctx.invoked_subcommand is None:
            #await ctx.send_help(ctx.command)
            e = discord.Embed(title="Emote help", color=discord.Color.dark_teal())
            e.description = f"`url` **- Get an emote's URL**\n`info` **- Get info about an emote**"
            await ctx.send(embed=e)

    @emote.group()
    async def url(self, ctx, emote: discord.PartialEmoji):
        """ Get an emote's URL """
        await ctx.send(emote.url)

    @emote.group()
    async def info(self, ctx, emote: discord.Emoji):
        """ Get info about an emote """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_author(name=emote.name, icon_url=emote.guild.icon_url)
        e.description = f"""
**Created on {default.date(emote.created_at)}**
**From** {emote.guild} (`{emote.guild_id}`)
**Emote ID:** `{emote.id}`
**Emote URL:** [Click here]({emote.url})
**Escaped:** \{emote}
"""
        e.set_thumbnail(url=emote.url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(HelpCog(bot))
