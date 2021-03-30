import discord, config, json, requests, random
from discord.ext import commands


class utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get someone's ID")
    async def id(self, ctx, member: discord.Member):
        """Get a server member's ID"""
        await ctx.send(member.id)


    @commands.command(brief="See someone's avatar", aliases=["av"])
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Shows the avatar of the specified user"""
        if not user:
            user = ctx.author
        e = discord.Embed(color=config.color)
        e.set_author(name=f"avatar of {user}", icon_url=user.avatar_url)
        e.set_image(url=user.avatar_url)
        await ctx.send(embed=e)
    
    
    @commands.command(brief="See server icon")
    async def servericon(self, ctx):
        """Shows the icon of the server you are in"""
        e = discord.Embed(color=config.color)
        e.set_author(name=f"Icon of {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)


    @commands.command(brief="Random selection")
    async def random(self, ctx, *args):
        """Select a random option out of the given options"""
        if not args:
            return await ctx.send("Please give more than 1 argument for me to choose from.")
        await ctx.send(f"I choose `{random.choice(args)}`.")

    @commands.command(brief="Host a poll")
    async def poll(self, ctx, *, args):
        """Make a yes/no poll"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        e = discord.Embed(color=config.color)
        e.description = args
        e.set_footer(text=f"Poll hosted by {ctx.message.author}")
        bm = await ctx.send(embed=e)
        await bm.add_reaction('<a:checkmark:813798012399779841>')
        await bm.add_reaction('<a:cross:813798012626141185>')

    @commands.command(brief="Say something")
    async def say(self, ctx, *, args):
        """Say something through the bot"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        e = discord.Embed(color=config.color)
        e.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        e.description = args
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(utility(bot))
