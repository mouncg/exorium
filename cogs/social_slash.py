import config
import discord
import gifs
import random
import aiohttp
import json
from discord.ext import commands
from utils import default as functions
from discord_slash import cog_ext, SlashContext


class slash(commands.Cog, name="Slash"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = ""

    @cog_ext.cog_slash(description="Slap someone", options=[{"name": "members", "description": "The member you want to slap.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're slapping the members.", "type": 3, "required": False}])
    async def slash_slap(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Slap the specified people"""
        if str(ctx.author.id) in str(members):
            return await ctx.send("You can't slap yourself, derp!")
        await functions.interactions(ctx, members, "slapped", 'slap', gifs.slap, reason)

    @cog_ext.cog_slash(description="Snuggle someone", options=[{"name": "members", "description": "The member you want to snuggle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're snuggling the members.", "type": 3, "required": False}])
    async def slash_snuggle(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Snuggle the specified people"""
        await functions.interactions(ctx, members, "snuggled", 'snuggle', gifs.snuggle, reason)

    @cog_ext.cog_slash(description="Hug someone", options=[{"name": "members", "description": "The member you want to hug.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're hugging the members.", "type": 3, "required": False}])
    async def slash_hug(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
       await functions.interactions(ctx, members, "hugged", 'hug', gifs.hug, reason, 'hug')

    @cog_ext.cog_slash(description="Bonk someone", options=[{"name": "members", "description": "The member you want to bonk.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're bonking the members.", "type": 3, "required": False}])
    async def slash_bonk(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Bonk the specified people"""
        await functions.interactions(ctx, members, "bonked", 'bonk', gifs.bonk, reason)

    @cog_ext.cog_slash(description="Boop someone", options=[{"name": "members", "description": "The member you want to boop.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're booping the members.", "type": 3, "required": False}])
    async def slash_boop(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Boop the specified people"""
        await functions.interactions(ctx, members, "booped", 'boop', gifs.boop, reason)

    @cog_ext.cog_slash(description="Smooch someone", options=[{"name": "members", "description": "The member you want to kiss.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're kissing the members.", "type": 3, "required": False}])
    async def slash_smooch(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Smooch the specified people"""
        await functions.interactions(ctx, members, "smooched", 'smooch', gifs.smooch, reason)

    @cog_ext.cog_slash(description="Lick someone", options=[{"name": "members", "description": "The member you want to lick.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're licking the members.", "type": 3, "required": False}])
    async def slash_lick(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Lick the specified people"""
        await functions.interactions(ctx, members, "licked", 'lick', gifs.lick, reason)

    @cog_ext.cog_slash(description="Give bellyrubs!", options=[{"name": "members", "description": "The member you want to bellyrub.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're bellyrubbing the members.", "type": 3, "required": False}])
    async def slash_bellyrub(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, members, "bellyrubbed", 'rub the belly of', gifs.bellyrub, reason)

    @cog_ext.cog_slash(description="Nuzzle someone", options=[{"name": "members", "description": "The member you want to nuzzle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're nuzzling the members.", "type": 3, "required": False}])
    async def slash_nuzzle(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Nuzzle the specified people"""
        await functions.interactions(ctx, members, "nuzzled", 'nuzzles', gifs.nuzzle, reason)

    @cog_ext.cog_slash(description="Cuddle someone", options=[{"name": "members", "description": "The member you want to cuddle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're cuddling the members.", "type": 3, "required": False}])
    async def slash_cuddle(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Cuddle the specified people"""
        await functions.interactions(ctx, members, "cuddled", 'cuddle', gifs.cuddle, reason)

    @cog_ext.cog_slash(description="Feed someone", options=[{"name": "members", "description": "The member you want to feed.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're feeding the members.", "type": 3, "required": False}])
    async def slash_feed(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Feed the specified people"""
        await functions.interactions(ctx, members, "fed", 'feed', gifs.feed, reason)

    @cog_ext.cog_slash(description="Glomp someone", options=[{"name": "members", "description": "The member you want to glomp.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're glomping the members.", "type": 3, "required": False}])
    async def slash_glomp(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Glomp on the specified people"""
        await functions.interactions(ctx, members, "glomped", 'glomp', gifs.glomp, reason)

    @cog_ext.cog_slash(description="Highfive someone", options=[{"name": "members", "description": "The member you want to highfive.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're highfiving the members.", "type": 3, "required": False}])
    async def slash_highfive(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Highfive the specified people"""
        await functions.interactions(ctx, members, "highfived", 'hivefive', gifs.highfive, reason)

    @cog_ext.cog_slash(description="Rawrrrr", options=[{"name": "members", "description": "The member you want to rawr at.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're rawring at the members.", "type": 3, "required": False}])
    async def slash_rawr(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Rawr at the specified people"""
        await functions.interactions(ctx, members, "rawred at", 'rawr at', gifs.rawr, reason)

    @cog_ext.cog_slash(description="Howl to the moon, or someone", options=[{"name": "members", "description": "The member you want to howl at.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're howl at the members.", "type": 3, "required": False}])
    async def slash_awoo(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Howl at the specified people"""
        await functions.interactions(ctx, members, "howled at", 'howl at', gifs.awoo)

    @cog_ext.cog_slash(description="pat someone!", options=[{"name": "members", "description": "The member you want to pat.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're patting the members.", "type": 3, "required": False}])
    async def slash_pat(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Pat the specified people"""
        await functions.interactions(ctx, members, "patted", 'pat', gifs.pet, 'pat', reason)

    @cog_ext.cog_slash(description="Gib cookie", options=[{"name": "members", "description": "The member you want to give a cookie to.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're giving a cookie to the members.", "type": 3, "required": False}])
    async def slash_cookie(self, ctx: SlashContext, members: commands.Greedy[discord.Member], *, reason=None):
        """Give cookies to the specified people"""
        await functions.interactions(ctx, members, "gave a cookie to", 'give a cookie to', gifs.cookie, reason)

    @cog_ext.cog_slash(description="Blushies!", options=[{"name": "members", "description": "The member you're blushing because of", "type": 6, "required": False}])
    async def slash_blush(self, ctx: SlashContext, members: commands.Greedy[discord.Member] = None):
        """Blush (optionally because of specified people)"""
        await functions.feelings(ctx, members, "blushes", gifs.blush)

    @cog_ext.cog_slash(description="Be happy", options=[{"name": "members", "description": "The member you're happy because of", "type": 6, "required": False}])
    async def slash_happy(self, ctx: SlashContext, members: commands.Greedy[discord.Member] = None):
        """Be happy (optionally because of specified people)"""
        await functions.feelings(ctx, members, "smiles", gifs.happy)

    @cog_ext.cog_slash(description="wag yer tail", options=[{"name": "members", "description": "The member you're wagging your tail because of", "type": 6, "required": False}])
    async def slash_wag(self, ctx: SlashContext, members: commands.Greedy[discord.Member] = None):
        """Wag your tail (Optionally because of specified people)"""
        await functions.feelings(ctx, members, "wags their tail", gifs.wag)

    @cog_ext.cog_slash(description="Quack quack!", options=[{"name": "members", "description": "The member you're quacking because of", "type": 6, "required": False}])
    async def slash_quack(self, ctx: SlashContext, members: commands.Greedy[discord.Member] = None):
        """Quack (Optionally because of specified people)"""
        duck_list = [f"https://random-d.uk/api/{random.randint(1,191)}.jpg", f"https://random-d.uk/api/{random.randint(1,42)}.gif"]
        await functions.feelings(ctx, members, "quacks", duck_list)

def setup(bot):
    bot.add_cog(slash(bot))
