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
        await functions.interactions(ctx, members, reason, "slap", "bad!", "slapped")

    @commands.command(brief="Snuggle someone")
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member], *, reason="being adorable"):
        await functions.interactions(ctx, members, reason, "snuggle", "how cute", "snuggled")

    @commands.command(brief="Hug someone")
    async def hug(self, ctx, members:commands.Greedy[discord.Member], *, reason="being lovely"):
        await functions.interactions(ctx, members, reason, "hug", "how lovely", "hugged")

    @commands.command(brief="Bonk someone")
    async def bonk(self, ctx, members: commands.Greedy[discord.Member], *, reason="bad!"):
        await functions.interactions(ctx, members, reason, "bonk", "how mean", "bonked")

    @commands.command(brief="Pet someone", aliases=["pat"])
    async def pet(self, ctx, members: commands.Greedy[discord.Member], *, reason="being a cutie"):
        await functions.interactions(ctx, members, reason, "pet", "how beautiful", "pet")

    @commands.command(brief="Boop someone")
    async def boop(self, ctx, members: commands.Greedy[discord.Member], *, reason="being adorable"):
        await functions.interactions(ctx, members, reason, "boop", "so soft", "booped")
    
    @commands.command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, members: commands.Greedy[discord.Member], *, reason="being lovely"):
        await functions.interactions(ctx, members, reason, "smooch", "lovely", "smooched")
        
    

def setup(bot):
    bot.add_cog(social(bot))
