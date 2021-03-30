from collections import Counter
from datetime import datetime

import random
import aiohttp
import config
import discord
import platform
import psutil
import time
from discord.ext import commands

from utils import default


class info(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot


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


    @commands.command(brief="The invites for exorium")
    async def invite(self, ctx):
        e = discord.Embed(color=config.color)
        e.description = f"""
You can invite me to your server [here](https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=335932630&scope=bot)
"""
# For alternative invite links, refer to [the website](https://bluewydev.github.io/exoriumbot)
#[needed permissions (recommended)](https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=335932630&scope=bot) - All permissions the bot needs.
#[admin permissions](https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=8&scope=bot) - administrator permissions (Use only when necessary)
#[no permissions](https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=0&scope=bot) no permissions at all (can break the bot in your guild)
        await ctx.send(embed=e)


    @commands.command(brief="Our privacy policy")
    async def privacy(self, ctx):
        e = discord.Embed(color=config.color)
        e.description = f"""
You can read our privacy policy [here](https://bluewydev.github.io/exoriumbot/src/pages/legal.html).
Want your data removed or got questions? mail to `bluewyechache@gmail.com`.
"""
        await ctx.send(embed=e)


    @commands.command(brief="Get support")
    async def support(self, ctx):
        e = discord.Embed(color=config.color)
        e.description = f"""
You can get help in the following ways:
- Send a mail to `bluewyechache@gmail.com`
- [Join the support server](https://discord.gg/CEHkNky)
"""
        await ctx.send(embed=e)


    @commands.command(brief="exo related links")
    async def links(self, ctx):
        e = discord.Embed(color=config.color)
        e.description = f"""
[[Status]](https://exorium.statuspage.io/) [[Repo]](https://github.com/ThePawKingdom/exorium/) [[Vote]](https://top.gg/bot/620990340630970425)

[[Website]](https://bluewydev.github.io/exoriumbot/) | [[Invite link]](https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=335932630&scope=bot)
"""
        await ctx.send(embed=e)


    @commands.command(brief="exorium statistics", aliases=["stats"])
    async def statistics(self, ctx):
        starttime = datetime.now().timestamp()
        print(starttime)
        print(datetime.now().timestamp())
        uptime = datetime.now().timestamp() - starttime
        channel_types = Counter(type(c) for c in self.bot.get_all_channels())
        voice = channel_types[discord.channel.VoiceChannel]
        text = channel_types[discord.channel.TextChannel]
        lastboot = str((datetime.utcfromtimestamp(uptime).strftime('%H hour(s), %M minute(s) and %S second(s)')))
        cpu_per = psutil.cpu_percent()
        cores = psutil.cpu_count()
        memory = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20
        storage_free = psutil.disk_usage('/').free >> 30
        e = discord.Embed(title="exorium statistics", color=config.color)
        e.description = f"""
__**About exorium**__
**Developers:** [Ayzen](https://discord.com/users/809057677716094997), [DuckMasterAl](https://discord.com/users/443217277580738571) & [Moksej](https://discord.com/users/345457928972533773)\n**Library:** [Discord.py {discord.__version__}](https://github.com/Rapptz/discord.py) <:python:758139554670313493>
    
__**statistics**__
**guilds:** {str(len(self.bot.guilds))}\n**users:** {str(len(self.bot.users))} (No intents to display correct number)\n**channels:**\nText <:channel:719660740050419935> {text:,}\nVoice <:voice:719660766269145118> {voice:,}
__**System**__
**Hosting OS:** `{platform.platform()}`\n**Cores:** `{cores}`\n**CPU:** `{cpu_per}%`\n**RAM:** `{mem_usage}/{memory} MB`\n**Storage:** `{storage_free} GB free`
"""
        e.set_image(url=config.banner)
        await ctx.send(embed=e)

    @commands.command(brief="See a server's info", aliases=["si", "sinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        gu = ctx.guild
        features = ", ".join(gu.features).lower().replace('_', ' ').title()
        if len(features) == 0:
            features = None
        if gu.mfa_level == 0:
            mfa = "Optional"
        else:
            mfa = "Required"

        e = discord.Embed(color=config.color)
        e.description = f"*Intents may cause human/bot count to display incorrectly.*"

        owner = await self.bot.fetch_user(gu.owner_id)
        e.add_field(name="__**Generic information**__",
                    value=f"**Owner:** {str(owner)}\n**Owner ID:**\n`{gu.owner_id}`\n**Created:** {default.date(ctx.guild.created_at)}\n**Region:** {str(gu.region)}\n**MFA: **{mfa}\n**Verification:** {str(ctx.guild.verification_level).capitalize()}", inline=True)
        e.add_field(name="__**Others**__",
                    value=f"**Humans:** {len(gu.bots)} ({len(gu.members)} total)\n**Bots:** {len(gu.humans)} ({len(gu.members)} total)\n**Text:** {len(gu.text_channels)} channels\n**Voice:** {len(gu.voice_channels)} channels", inline=True)
        if features is not None:
            e.add_field(name="__**Server features**__", value=features, inline=False)
        e.set_author(name=f"{gu.name} information", icon_url=gu.icon_url)
        e.set_footer(text=f"Guild ID: {gu.id}")
        e.set_thumbnail(url=gu.icon_url)
        e.set_image(url=gu.banner_url)
        await ctx.send(embed=e)

        
    @commands.command(brief="See a user's info", aliases=["ui"])
    @commands.guild_only()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author
        
        if user.is_on_mobile():
            appl = "On mobile"
        else:
            appl = "On desktop/website"
    
        if user.bot:
            bot = "Yes"
        else:
            bot = "No"
            
        if user.public_flags.verified_bot:
            botv = "Yes"
        else:
            botv = "No"
    
        e = discord.Embed(color=config.color)
        e.set_author(name=user.name, icon_url=user.avatar_url)
        stuff = f" (verified: {botv})" if user.public_flags.verified_bot else ""
        e.add_field(name="__**Generic information**__",
                    value=f"**Username:** {user}\n**User ID:** {user.id}\n**Created:** {default.date(user.created_at)}\n**Joined:** {default.date(user.joined_at)}\n**Avatar URL:** [Click here]({user.avatar_url})\n**Application:** {appl}\n**Bot:** {bot}{stuff}", inline=True)
        
        if user.public_flags.staff:
            staff = "Yes"
        else:
            staff = "No"

        if user.public_flags.hypesquad_balance:
            hs = "Balance"
        elif user.public_flags.hypesquad_brilliance:
            hs = "Brilliance"
        elif user.public_flags.hypesquad_bravery:
            hs = "Bravery"
        elif user.public_flags.hypesquad is False:
            hs = "None"

        if user.public_flags.partner:
            partner = "Yes"
        else:
            partner = "No"

        if user.public_flags.bug_hunter:
            bh = "Yes (1)"
        elif user.public_flags.bug_hunter_level_2:
            bh = "Yes (2)"
        else:
            bh = "No"

        if user.public_flags.early_supporter:
            es = "Yes"
        else:
            es = "No"

        if user.public_flags.value == 0:
            value = "None"
        else:
            value = user.public_flags.value
            
        if value != "None":
            e.add_field(name="__**Public flags**__",
                        value=f"**Discord staff:** {staff}\n**Discord partner:** {partner}\n**Early supporter:** {es}\n**Bug hunter:** {bh}\n**Hypesquad:** {hs}\n**Flag value:** {value}", inline=True)
        
        uroles = []
        for role in user.roles:
            if role.is_default():
                continue
            uroles.append(role.mention)
            
        uroles.reverse()
        
        if len(uroles) > 10:
            uroles = [f"{', '.join(uroles[:10])} (+{len(user.roles) - 11})"]
        
        if len(uroles) > 0:
            e.add_field(name=f"__**Roles ({len(user.roles) - 1})**__",
                        value=", ".join(uroles), inline=False)
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)


    @commands.group(brief="Emote related commands", aliases=["emoji"])
    async def emote(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(color=config.color)
            e.set_author(name="Emote command help", icon_url=self.bot.user.avatar_url)
            e.description = f"""
*Please provide an emote behind the command (no default emotes),
the info command only displays info from mutual server emotes.*

{ctx.prefix}emote url <emote> | **Get emote URL**
{ctx.prefix}emote info <emote> | **Get emote information**
"""
            await ctx.send(embed=e)

    @emote.command(brief="Get emote URL")
    async def url(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)
                      
    @emote.command(brief="Get emote information")
    async def info(self, ctx, emoji: discord.Emoji):
        e = discord.Embed(color=config.color)
        e.description = f"""
**Name:** {emoji.name}
**Created:** {default.date(emoji.created_at)}
**Emote ID:** `{emoji.id}`
**Escaped:**""" + f"`{emoji}`" + f"""
**Emote link**: [Click here]({emoji.url})
"""

        e.set_author(name=f"Emote from {emoji.guild}", icon_url=emoji.guild.icon_url)
        e.set_thumbnail(url=emoji.url)
        await ctx.send(embed=e)


    @commands.command(brief="Suggest something for exo")
    async def suggest(self, ctx, *, args):
        channel = self.bot.get_channel(769132481252818954)
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
        e = discord.Embed(color=config.green)
        e.set_author(name=f"Suggestion from {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        e.description = args
        e.set_footer(text="Cast your votes!")
        ses = await channel.send(embed=e)
        await ses.add_reaction('<a:checkmark:813798012399779841>')
        await ses.add_reaction('<a:cross:813798012626141185>')
        await ctx.send("The suggestion was sent successfully:")
        se = discord.Embed(color=config.green)
        se.description = args
        await ctx.send(embed=se)

    @commands.command(brief="random animal fact")
    async def fact(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/dog") as r:
                async with cs.get("https://some-random-api.ml/facts/cat") as c:
                    async with cs.get("https://some-random-api.ml/facts/panda") as p:
                        async with cs.get("https://some-random-api.ml/facts/fox") as f:
                            async with cs.get("https://some-random-api.ml/facts/bird") as b:
                                async with cs.get("https://some-random-api.ml/facts/koala") as k:
            
                                    facts = [r, c, p, f, b, k]
                                    rc = random.choice(facts)
                                    js = await rc.json()

                                    await ctx.send(js['fact'])


    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
    #    if isinstance(error, commands.CommandNotFound):
    #        pass
    #    else:
    #        embed = discord.Embed(description=str(error), color=discord.Color.red())
    #        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
