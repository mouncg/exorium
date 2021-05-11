import discord
import config
import time
import aiohttp
import psutil
import platform
import asyncio

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
    @commands.cooldown(1, 2, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def invite(self, ctx):
        """ Invite Esquire to your server """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f'{config.inv}[Default perms]({config.invite})\n {config.inv}[All perms]({config.invite2})'
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def privacy(self, ctx):
        """ Read our privacy policy """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"Read Esquire's privacy policy [here]({config.privacy})."
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def support(self, ctx):
        """ Get support with Esquire """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"""
You can get support here:
- [support server]({config.support})
- [Github issue](https://github.com/flitzstudios/exorium/issues/new)
- [Email us](https://quacky.xyz/email?email=flitzdevelopment@gmail.com)
"""
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """ Make suggestions for Esquire """
        channel = self.bot.get_channel(839962330787479592)
        if len(suggestion) >= 500:
            return await ctx.send(f"Please make your suggestion shorter then 500 characters.")
        e = discord.Embed(color=discord.Color.orange())
        e.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
        e.description = suggestion
        ra = await channel.send(embed=e)
        await ra.add_reaction(config.checkmark)
        await ra.add_reaction(config.crossmark)
        await ctx.send(f"Your suggestion was recorded in our support server.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def id(self, ctx, member: discord.Member):
        """ Get a user's ID """
        await ctx.reply(member.id)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def av(self, ctx, user: discord.Member = None):
        """ Get a user's avatar """
        if not user:
            user = ctx.message.author

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_image(url=user.avatar_url)
        e.set_footer(text=f"avatar: {user}")
        await ctx.send(embed=e)

    @commands.command(aliases=["si"])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """ Get information about the server """

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
    @commands.cooldown(1, 2, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def servericon(self, ctx):
        """ Get the server's icon """
        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(add_reactions=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
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
        Fenny = await self.bot.fetch_user(699686304388087858)
        Rika = await self.bot.fetch_user(750470053300011070)
        devs = [f"{x.name}#{x.discriminator}" for x in
                self.bot.get_guild(755068089233834074).get_role(828339695314403378).members]
        dev1 = ', '.join(devs)

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.set_image(url="https://cdn.bluewy.xyz/yerZ.png")

        users = sum(x.member_count for x in self.bot.guilds)

        e.description = f"""
__**About**__
Developers:
- **[{Rika}](https://discordrep.com/u/750470053300011070#)**
- **[{Moksej}](https://discordrep.com/u/345457928972533773#)**
- **[{Duck}](https://discordrep.com/u/443217277580738571#)**
- **[{Fenny}](https://discordrep.com/u/699686304388087858#)**

Library: [enhanced dpy {discord.__version__}](https://github.com/iDutchy/discord.py)

__**Statistics**__
**{len(self.bot.guilds)}** Guilds
**{users:,}** Users
**{text}** text & **{voice}** voice channels

__**System**__
Hosted on **{platform.platform()}**
**{core}** cores
**{cpup}**% CPU load
**{mem_usage}**/**{mem}** MB memory used
**{storage_free}** GB storage free 
"""

        await ctx.send(embed=e)

    @commands.command()
    async def about(self, ctx):
        """ About exorium """
        Flitz = await self.bot.fetch_user(809057677716094997)

        ae = discord.Embed(color=discord.Color.dark_teal())
        ae.set_image(url="https://cdn.bluewy.xyz/yerZ.png")
        ae.set_author(name=f"About {self.bot.user}",icon_url=self.bot.user.avatar_url)
        ae.description = f"""
Created by **[{Flitz}](https://discordrep.com/u/809057677716094997)**
Creation date: **{default.date(self.bot.user.created_at)}**
Developed and owned by Flitz Studios © 2021

Lib & version: **[Enhanced discord.py {discord.__version__}
Links: **[Support]({config.support})** | **[Invite]({config.invite})** | **[Privacy]({config.privacy})**
"""
        await ctx.send(embed=ae)

    @commands.group(aliases=["emoji", "e"])
    async def emote(self, ctx):
        """ Get emote info/url """
        if ctx.invoked_subcommand is None:
            #await ctx.send_help(ctx.command)
            e = discord.Embed(title="Emote help", color=discord.Color.dark_teal())
            e.description = f"`url` **- Get an emote's URL**\n`info` **- Get info about an emote**"
            await ctx.send(embed=e)

    @emote.group(aliases=["link", "u"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def url(self, ctx, emote: discord.PartialEmoji):
        """ Get an emote's URL """
        await ctx.send(emote.url)

    @emote.group(aliases=["i"])
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def review(self, ctx, *, review):
        """ Review our bot! """
        channel = self.bot.get_channel(839962350521548871)
        e1 = discord.Embed(color=discord.Color.dark_teal())
        e1.set_author(name=f'From {ctx.author}', icon_url=ctx.author.avatar_url)
        e1.description = review
        await channel.send(embed=e1)
        await ctx.send("Thank you! Your review has been recorded in our support server.")

    @commands.group(aliases=["b"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def binary(self, ctx):
        """ Encode/decode binary """
        if ctx.invoked_subcommand is None:
            e = discord.Embed(color=discord.Color.dark_teal(), title="Binary help")
            e.description = f"`encode` **- Encode text to binary**" \
                            f"\n`decode` **- Decode binary to text**"
            await ctx.send(embed=e)

    @binary.group(aliases=["e"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def encode(self, ctx, *, text):
        """ Encode text to binary """
        if len(text) > 200:
            return await ctx.send("Please limit it to 200 characters maximum, the bot will error out otherwise.")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?text={text}") as r:
                js = await r.json()

                await ctx.send(js['binary'])

    @binary.group(aliases=["d"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def decode(self, ctx, *, binary):
        """ Decode binary to text """
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/binary?decode={binary}") as r:
                js = await r.json()

                await ctx.send(js['text'])

    @commands.group(aliases=["b64"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def base64(self, ctx):
        """ Encode/Decode base64 """
        if ctx.invoked_subcommand is None:
            e = discord.Embed(color=discord.Color.dark_teal(), title="Base64 help")
            e.description = f"`encode` **- Encode text to base64**" \
                            f"\n`decode` **- Decode base64 to text**"
            await ctx.send(embed=e)

    @base64.group(aliases=["e"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def encode(self, ctx, *, text):
        """ Encode text to base64 """
        if len(text) > 1500:
            return await ctx.send('Please limit it to 1500 characters maximum, the bot will error out otherwise.')
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/base64?encode={text}") as r:
                js = await r.json()

                await ctx.send(js['base64'])

    @base64.group(aliases=["d"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def decode(self, ctx, *, base64):
        """ Decode base64 to text """
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/base64?decode={base64}") as r:
                js = await r.json()

                await ctx.send(js['text'])

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def announce(self, ctx, channel: discord.TextChannel, *, desc):
        """ Announce something """
        if not channel:
            return await ctx.send('Please provide a channel to use.')
        if len(desc) > 2000:
            return await ctx.send('Please make your announcement shorter then 2000 characters.')
        if len(desc) < 2000:
            e = discord.Embed(color=discord.Color.dark_teal())
            e.description = f"Do you want the message embedded?"

            checkmark = '<a:checkmark:813798012399779841>'
            crossmark = '<a:cross:813798012626141185>'

            def check(r, u):
                return u.id == ctx.author.id and r.message.id == checkmsg.id

            try:
                checkmsg = await ctx.send(embed=e)
                await checkmsg.add_reaction(checkmark)
                await checkmsg.add_reaction(crossmark)
                react, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)

                if str(react) == checkmark:
                    try:
                        await checkmsg.clear_reactions()
                    except Exception:
                        pass
                    e = discord.Embed(color=discord.Color.random(), description=desc)
                    e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await channel.send(embed=e)

                    embed = discord.Embed(color=discord.Color.green(), description=f"Sent embedded announcement in **{channel}**.")
                    await checkmsg.edit(embed=embed)
                    return

                if str(react) == crossmark:
                    try:
                        await checkmsg.clear_reactions()
                    except Exception:
                        pass
                    await channel.send(desc)

                    embed2 = discord.Embed(color=discord.Color.green(), description=f"Sent plain announcement in **{channel}**.")
                    await checkmsg.edit(embed=embed2)
                    return

            except asyncio.TimeoutError:
                try:
                    await checkmsg.clear_reactions()
                except Exception:
                    pass
                etimeout = discord.Embed(color=discord.Color.dark_red(), description=f"Command timed out, canceling...")
                return await checkmsg.edit(embed=etimeout)


def setup(bot):
    bot.add_cog(HelpCog(bot))
