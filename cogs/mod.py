import discord, config
from discord.ext import commands

class mod(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Ban someone")
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            if member == ctx.message.author:
                return await ctx.send("You can not ban yourself, please try someone else.")
        else:
            await ctx.send('Just a minor test')

def setup(bot):
    bot.add_cog(mod(bot))
