import discord
import typing
import time
import asyncio
from discord.ext import commands
from utils import default

class owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="shutdown", aliases=["logout"])
    @commands.is_owner()
    async def jsk_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """

        await ctx.send("Logging out now")
        await ctx.bot.logout()


    @commands.command(brief="unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """
        Unloads A.K.A. disables the given cog
        """
        if cog == 'cogs.owner':
            await ctx.send('**You cannot unload the owner cog as this cog allows unloading/reloading/loading cogs.**')
            return
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'Successfully unloaded`{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to unload {cog}\n```py\n{e}\n```')


    @commands.command(brief="load a cog")
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """
        Loads A.K.A. enables the given cog
        """
        try:
            self.bot.load_extension(cog)
            await ctx.send(f'Successfully loaded `{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')


    @commands.command(brief="Reload a cog")
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        """
        Reloads A.K.A. restarts the given cog
        """
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f'Successfully reloaded `{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')


    @commands.group(brief="Change bot appearance")
    @commands.is_owner()
    async def change(self, ctx):
        """
        Group command for status changing
        """
        if ctx.invoked_subcommand is None:
            pass


    @change.command(brief="Change playing status")
    @commands.is_owner()
    async def playing(self, ctx, *, playing: str):
        """
        Change the bot's playing status
        """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing),
                status=discord.Status.online
            )
            await ctx.send(f"Successfully changed Playing status to:\n{playing}")
            await ctx.message.delete()
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(e)


    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, id):
        """
        Forcibly leave a guild through ID
        """
        
        checkmark = '<a:checkmark:813798012399779841>'
        crossmark = '<a:cross:813798012626141185>'

        def check(r, u):
            return u.id == ctx.author.id and r.message.id == checkmsg.id

        guild = await self.bot.fetch_guild(id)
        e = discord.Embed(color=discord.Color.red())
        e.set_thumbnail(url=guild.icon_url)
        e.description = f"""
**Guild name:** {guild.name}
**Guild owner:** {await self.bot.fetch_user(guild.owner_id)}
**Guild owner ID:** {guild.owner_id}
**{len(guild.humans)}** humans & **{len(guild.bots)}** bots

Created on {default.date(guild.created_at)}.
__**Are you sure you want me to leave this guild?**__
"""
        checkmsg = await ctx.send(embed=e)
        await checkmsg.add_reaction(checkmark)
        await checkmsg.add_reaction(crossmark)
        react, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        
        if str(react) == checkmark:
            try:
                await checkmsg.clear_reactions()
            except Exception:
                pass
            await checkmsg.edit(content="Okay, leaving this guild.")
            await ctx.guild.leave()
            return
        
        if str(react) == crossmark:
            try:
                await checkmsg.clear_reactions()
            except Exception:
                pass
            await checkmsg.edit(content="Okay, i will stay in this guild.")
            return
        
        except asyncio.TimeoutError:
            try:
                await checkmsg.clear_reactions()
            except Exception:
                pass
            return await checkmsg.edit(content="Command timed out, canceling...")


    @commands.group(name='blacklist', invoke_without_command=True, enabled=True)  # invoke_without_command means you can have separate permissions/cooldowns for each subcommand
    @commands.is_owner()
    async def blacklist(self, ctx):
        """
        Group command for blacklisting
        """
        await ctx.send_help(ctx.command)


    @blacklist.command(name='user', enabled=True)
    @commands.is_owner()
    async def blacklist_user(self, ctx, user: typing.Union[discord.User, int], *, reason: str):
        """
        Blacklist or unblacklist a user
        """
        try:
            if isinstance(user, discord.User):
                print('pass discord.User')
                user = user
            elif isinstance(user, int):
                user = await self.bot.fetch_user(user)
            print('fetch user')
        except Exception as e:
            await ctx.send(f"Failed to find the user: `{e}`")
            print('caught exception')
        
        try:
            self.bot.blacklist[user.id]
            self.bot.database.execute(f"DELETE FROM blacklist WHERE id = {user.id}")
            self.bot.blacklist.pop(user.id)
            await ctx.send(f"unblacklisted {user}")
            print('unblacklisted')
        except Exception:
            self.bot.database.execute(f"INSERT INTO blacklist(id, reason) VALUES({user.id}, {reason})")
            self.bot.blacklist[user.id] = reason
            await ctx.send(f"blacklisted {user}")
            print('blacklisted')


    @blacklist.command(name='server', enabled=True)
    @commands.is_owner()
    async def blacklist_server(self, ctx, server: int, *, reason: str):
        """
        Blacklist or unblacklist a server
        """
        if not self.bot.get_guild(server):
            return await ctx.send("That server was not found make sure the ID is correct or if I'm in the server.")
        try:
            self.bot.blacklist[server]
            self.bot.database.execute(f"DELETE FROM blacklist WHERE id = {server}")
            self.bot.blacklist.pop(server)
            await ctx.send(f"unblacklisted {server}")          
        except Exception:
            self.bot.database.execute(f"INSERT INTO blacklist(id, reason) VALUES({server}, {reason})")
            self.bot.blacklist[server] = reason
            await ctx.send(f"blacklisted {server}")

            
def setup(bot):
    bot.add_cog(owner(bot))
