import discord, config
from discord.ext import commands

def admin():
    async def predicate(ctx):
        bot = ctx.bot
        guild = bot.get_guild(755068089233834074)
        role = guild.get_role(828339695314403378)
        return ctx.author.id in [x.id for x in role.members]
    return commands.check(predicate)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @admin()
    async def load(self, ctx, *, cog):
        self.bot.load_extension(f'cogs.{cog}')
        await ctx.send(f"{config.checkmark} loaded cog **{cog}**")
        print(f"{ctx.author} loaded cog \"{cog}\" successfully.")

    @commands.command()
    @admin()
    async def reload(self, ctx, *, cog='~'):
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

def setup(bot):
    bot.add_cog(Admin(bot))
