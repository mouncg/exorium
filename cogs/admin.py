import config
import discord
import asyncio
from discord.ext import commands
from utils import default


def admin():
    async def predicate(ctx):
        return ctx.author.id == 809057677716094997 or ctx.author.id == 345457928972533773 or ctx.author.id == 443217277580738571
    return commands.check(predicate)


class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "<:locked:719660754512642160>"

    @commands.command()
    @admin()
    async def load(self, ctx, *, cog):
        """
        Load the specified cog
        """
        self.bot.load_extension(f'cogs.{cog}')
        await ctx.send(f"{config.checkmark} loaded cog **{cog}**")
        print(f"{ctx.author} loaded cog \"{cog}\" successfully.")

    @commands.command()
    @admin()
    async def reload(self, ctx, *, cog='~'):
        """
        Reload a specified/all cogs
        """
        if cog == '~':
            for extension in config.extensions:
                self.bot.reload_extension(extension)
            await ctx.send(f"{config.checkmark} Reloaded all cogs successfully.")
            print(f"{ctx.author} reloaded all cogs successfully.")
        else:
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f"{config.checkmark} Reloaded cog **{cog}**")
            print(f"{ctx.author} reloaded \"{cog}\" successfully.")

    @commands.command()
    @admin()
    async def unload(self, ctx, *, cog):
        """
        Unload the specified cog
        """
        if cog == 'admin':
            return await ctx.send(f"{config.crossmark} Could not unload cog `admin`.")
        self.bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f"{config.checkmark} Unloaded cog **{cog}**")
        print(f"{ctx.author} unloaded \"{cog}\" Successfully.")

    @commands.command()
    @admin()
    async def shutdown(self, ctx):
        """ Shuts down the bot. """
        await ctx.send('Shutting down.')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down.'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @admin()
    async def leave(self, ctx, id):
        """
        Forcibly leave a guild through ID
        """

        checkmark = '<a:checkmark:813798012399779841>'
        crossmark = '<a:cross:813798012626141185>'

        def check(r, u):
            return u.id == ctx.author.id and r.message.id == checkmsg.id

        try:
            guild = await self.bot.fetch_guild(id)
        except Exception:
            return await ctx.send('This is not a discord server i\'m in.')
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
                eleave = discord.Embed(color=discord.Color.dark_red(), description=f"Okay, leaving this guild.")
                await checkmsg.edit(embed=eleave)
                await guild.leave()
                return

            if str(react) == crossmark:
                try:
                    await checkmsg.clear_reactions()
                except Exception:
                    pass
                estay = discord.Embed(color=discord.Color.green(), description=f"Okay, staying in this guild.")
                await checkmsg.edit(embed=estay)
                return

        except asyncio.TimeoutError:
            try:
                await checkmsg.clear_reactions()
            except Exception:
                pass
            etimeout = discord.Embed(color=discord.Color.dark_red(), description=f"Command timed out, canceling...")
            return await checkmsg.edit(embed=etimeout)


def setup(bot):
    bot.add_cog(Admin(bot))
