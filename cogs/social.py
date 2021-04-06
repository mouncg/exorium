import config
import discord
import gifs
import random
import aiohttp
import json
from discord.ext import commands
from utils import default as functions


class social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Slap someone", enabled=False)
    async def slap(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Slap the specified people"""
        if str(ctx.author.id) in str(members):
            return await ctx.send("You can't slap yourself, derp!")
        await functions.interactions(ctx, members, "slap", "slaps")

    @commands.command(brief="Snuggle someone")
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Snuggle the specified people"""
        await functions.social(ctx, members, "snuggled", gifs.snuggle, reason)

    @commands.command(brief="Hug someone")
    async def hug(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
       await functions.interactions(ctx, members, "hugged", gifs.hug, reason, 'hug')

    @commands.command(brief="Bonk someone")
    async def bonk(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Bonk the specified people"""
        await functions.interactions(ctx, members, "bonked", gifs.bonk, reason)

    @commands.command(brief="Boop someone")
    async def boop(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Boop the specified people"""
        await functions.interactions(ctx, members, "booped", gifs.boop, reason)

    @commands.command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Smooch the specified people"""
        await functions.interactions(ctx, members, "smooched", gifs.smooch, reason)

    @commands.command(brief="Lick someone")
    async def lick(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Lick the specified people"""
        await functions.interactions(ctx, members, "licked", gifs.lick, reason)

    @commands.command(brief="Give bellyrubs!")
    async def bellyrub(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, members, "bellyrubbed", gifs.bellyrub, reason)

    @commands.command(brief="Cuddle someone")
    async def cuddle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Cuddle the specified people"""
        await functions.interactions(ctx, members, "cuddled", gifs.cuddle, reason)

    @commands.command(brief="Feed someone")
    async def feed(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Feed the specified people"""
        await functions.interactions(ctx, members, "fed", gifs.feed, reason)

    @commands.command(brief="Glomp someone")
    async def glomp(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Glomp on the specified people"""
        await functions.interactions(ctx, members, "glomped", gifs.glomp, reason)

    @commands.command(brief="Highfive someone")
    async def highfive(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Highfive the specified people"""
        await functions.interactions(ctx, members, "highfived", gifs.highfive, reason)

    @commands.command(brief="Rawrrrr")
    async def rawr(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Rawr at the specified people"""
        await functions.interactions(ctx, members, "rawred at", gifs.rawr, reason)

    @commands.command(brief="Howl to the moon, or someone", aliases=["howl"])
    async def awoo(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Howl at the specified people"""
        await functions.interactions(ctx, members, "howled at", gifs.awoo)

    @commands.command(brief="pat someone!", aliases=["pet"])
    async def pat(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Pat the specified people"""
        await functions.interactions(ctx, members, "patted", gifs.pet, 'pat', reason)

    @commands.command(brief="Gib cookie")
    async def cookie(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give cookies to the specified people"""
        await functions.interactions(ctx, members, "gave a cookie to", gifs.cookie, reason)

    @commands.command(brief="Blushies!")
    async def blush(self, ctx, members: commands.Greedy[discord.Member] = None):
        """Blush (optionally because of specified people)"""
        await functions.feelings(ctx, members, "blushes", gifs.blush)

    @commands.command(brief="Be happy")
    async def happy(self, ctx, members: commands.Greedy[discord.Member] = None):
        """Be happy (optionally because of specified people)"""
        await functions.feelings(ctx, members, "smiles", gifs.happy)

    @commands.command(brief="wag yer tail")
    async def wag(self, ctx, members: commands.Greedy[discord.Member] = None):
        """Wag your tail (Optionally because of specified people)"""
        await functions.feelings(ctx, members, "wags their tail", gifs.wag)

def setup(bot):
    bot.add_cog(social(bot))
