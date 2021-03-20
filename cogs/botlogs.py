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
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} - {ctx.guild.name} | {ctx.author} > {ctx.message.clean_content}") 
    #    log = self.bot.get_channel(755138117488345118)
        
    #    e = discord.Embed(color=config.color)
    #    e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #    e.description = f"""
#**Message content:**
#{ctx.message.content}

#**Author ID:** [{ctx.author.id}](https://discord.com/users/{ctx.author.id})

#**Guild:** {ctx.guild.name} (`{ctx.guild.id}`) 
#"""
#        e.set_footer(text=datetime.now().__format__('%a %d %b %y, %H:%M'))
#        e.set_thumbnail(url=ctx.guild.icon_url)
#        await log.send(embed=e)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log = self.bot.get_channel(762203326519181312)
        
        e = discord.Embed(color=config.green)
        e.set_author(name="Joined a new guild", icon_url=self.bot.user.avatar_url)
        e.set_thumbnail(url=guild.icon_url)

        owner = await self.bot.fetch_user(guild.owner_id)

        members = len(guild.humans)
        bots = len(guild.bots)
        text = len(guild.text_channels)
        voice = len(guild.voice_channels)

        e.description = f"""
**Guild name:** {guild.name} (`{guild.id}`)
**Guild owner:** {str(owner)} (`{guild.owner_id}`)
**Created:** {default.date(guild.created_at)}
**Members:** {members} humans & {bots} bots
**Channels:** {text} text channels & {voice} vc's
"""
        await log.send(embed=e)

        print(f"Joined guild {guild.name}. Check the server logs in exorium support for more information.")
              
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log = self.bot.get_channel(762203326519181312)

        e = discord.Embed(color=config.red)
        e.set_author(name="Left a guild", icon_url=self.bot.user.avatar_url)
        e.set_thumbnail(url=guild.icon_url)

        owner = await self.bot.fetch_user(guild.owner_id)

        members = len(guild.humans)
        bots = len(guild.bots)
        text = len(guild.text_channels)
        voice = len(guild.voice_channels)

        e.description = f"""
**Guild name:** {guild.name} (`{guild.id}`)
**Guild owner:** {str(owner)} (`{guild.owner_id}`)
**Created:** {default.date(guild.created_at)}
**Members:** {members} humans & {bots} bots
**Channels:** {text} text channels & {voice} vc's
"""
        await log.send(embed=e)

        print(f"Left guild {guild.name}. Check the server logs in exorium support for more information.")
              
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.DisabledCommand):
            return await ctx.send(f"{config.emotecross} This command has been disabled by the developers.")

        if isinstance(err, commands.MissingRequiredArgument):
            return await ctx.send(f"{config.emotecross} You are missing required arguments. Try `{ctx.clean_prefix}help <command>` for more information.")

        if isinstance(err, commands.NoPrivateMessage):
            return await ctx.send(f"{config.emotecross} This command is restricted to servers only.")

        if isinstance(err, commands.TooManyArguments):
            return await ctx.send(f"You specified more then needed arguments and/or wrong arguments. Use `{ctx.clean_prefix}help <command>` for more information.")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Tries to re-run a command when a message gets edited! """
        if after.author.bot is True or before.content == after.content:
            return
        prefixes = commands.when_mentioned_or('exo ')(self.bot, after)
        if after.content.startswith(tuple(prefixes)):
            ctx = await self.bot.get_context(after)
            msg = await self.bot.invoke(ctx)
              

def setup(bot):
    bot.add_cog(botlogs(bot))
