import discord, config, json, requests, random
from discord.ext import commands

class images(commands.Cog, name="Images"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="Get a gay overlay for your avatar", aliases=["prideav"])
    async def gay(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.message.author
        link = f"https://some-random-api.ml/canvas/gay/?avatar={user.avatar_url}"
        e = discord.Embed(color=config.color)
        e.set_author(name=f"Gay avatar of {user}", icon_url=user.avatar_url)
        e.set_image(url=link)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(images(bot))
