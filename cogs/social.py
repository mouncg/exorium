import discord, random, gifs
from discord.ext import commands
from outsources import functions

class social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Slap someone")
    async def slap(self, ctx, members: commands.Greedy[discord.Member], *, reason="Being bad"):
        if str(ctx.message.author.id) in str(members):
            await ctx.send("You can't slap yourself, derp!")
            return
        await functions.interactions(ctx, members, reason, "slap", "bad!", "slapped", "slap")

    @commands.command(brief="Snuggle someone")
    async def snuggle(ctx, members: commands.Greedy[discord.Member], *, reason="being adorable"):
        await functions.interactions(ctx, members, reason, "snuggle", "how cute", "snuggled", snuggle)


def setup(bot):
    bot.add_cog(social(bot))
