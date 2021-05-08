import config
import discord
import gifs
import random
import aiohttp
import json
import traceback
from discord.ext import commands
from utils import default as functions
from discord_slash import cog_ext, SlashContext


class slash(commands.Cog, name="Slash"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "<:slash:833803136199032882>"

    @cog_ext.cog_slash(name="slap", description="Slap someone", options=[{"name": "member", "description":"The member you want to slap.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're slapping the member.", "type": 3, "required": False}])
    async def slash_slap(self, ctx: SlashContext, member, *, reason=None):
        """Slap the specified people"""
        if str(ctx.author.id) == str(member):
            return await ctx.send("You can't slap yourself, derp!")
        await functions.interactions(ctx, [member], "slapped", 'slap', gifs.slap, reason)

    @cog_ext.cog_slash(name="snuggle",  description="Snuggle someone", options=[{"name": "member", "description":"The member you want to snuggle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're snuggling the member.", "type": 3, "required": False}])
    async def slash_snuggle(self, ctx: SlashContext, member, *, reason=None):
        """Snuggle the specified people"""
        await functions.interactions(ctx, [member], "snuggled", 'snuggle', gifs.snuggle, reason)

    @cog_ext.cog_slash(name="hug",  description="Hug someone", options=[{"name": "member", "description":"The member you want to hug.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're hugging the member.", "type": 3, "required": False}])
    async def slash_hug(self, ctx: SlashContext, member, *, reason=None):
       await functions.interactions(ctx, [member], "hugged", 'hug', gifs.hug, reason, 'hug')

    @cog_ext.cog_slash(name="bonk", description="Bonk someone", options=[{"name": "member", "description":"The member you want to bonk.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're bonking the member.", "type": 3, "required": False}])
    async def slash_bonk(self, ctx: SlashContext, member, *, reason=None):
        """Bonk the specified people"""
        await functions.interactions(ctx, [member], "bonked", 'bonk', gifs.bonk, reason)

    @cog_ext.cog_slash(name="boop", description="Boop someone", options=[{"name": "member", "description":"The member you want to boop.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're booping the member.", "type": 3, "required": False}])
    async def slash_boop(self, ctx: SlashContext, member, *, reason=None):
        """Boop the specified people"""
        await functions.interactions(ctx, [member], "booped", 'boop', gifs.boop, reason)

    @cog_ext.cog_slash(name="smooch", description="Smooch someone", options=[{"name": "member", "description":"The member you want to kiss.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're kissing the member.", "type": 3, "required": False}])
    async def slash_smooch(self, ctx: SlashContext, member, *, reason=None):
        """Smooch the specified people"""
        await functions.interactions(ctx, [member], "smooched", 'smooch', gifs.smooch, reason)

    @cog_ext.cog_slash(name="lick", description="Lick someone", options=[{"name": "member", "description":"The member you want to lick.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're licking the member.", "type": 3, "required": False}])
    async def slash_lick(self, ctx: SlashContext, member, *, reason=None):
        """Lick the specified people"""
        await functions.interactions(ctx, [member], "licked", 'lick', gifs.lick, reason)

    @cog_ext.cog_slash(name="bellyrub", description="Give bellyrubs!", options=[{"name": "member", "description":"The member you want to bellyrub.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're bellyrubbing the member.", "type": 3, "required": False}])
    async def slash_bellyrub(self, ctx: SlashContext, member, *, reason=None):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, [member], "bellyrubbed", 'rub the belly of', gifs.bellyrub, reason)

    @cog_ext.cog_slash(name="nuzzle", description="Nuzzle someone", options=[{"name": "member", "description":"The member you want to nuzzle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're nuzzling the member.", "type": 3, "required": False}])
    async def slash_nuzzle(self, ctx: SlashContext, member, *, reason=None):
        """Nuzzle the specified people"""
        await functions.interactions(ctx, [member], "nuzzled", 'nuzzles', gifs.nuzzle, reason)

    @cog_ext.cog_slash(name="cuddle",  description="Cuddle someone", options=[{"name": "member", "description":"The member you want to cuddle.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're cuddling the member.", "type": 3, "required": False}])
    async def slash_cuddle(self, ctx: SlashContext, member, *, reason=None):
        """Cuddle the specified people"""
        await functions.interactions(ctx, [member], "cuddled", 'cuddle', gifs.cuddle, reason)

    @cog_ext.cog_slash(name="feed",  description="Feed someone", options=[{"name": "member", "description":"The member you want to feed.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're feeding the member.", "type": 3, "required": False}])
    async def slash_feed(self, ctx: SlashContext, member, *, reason=None):
        """Feed the specified people"""
        await functions.interactions(ctx, [member], "fed", 'feed', gifs.feed, reason)

    @cog_ext.cog_slash(name="glomp",  description="Glomp someone", options=[{"name": "member", "description":"The member you want to glomp.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're glomping the member.", "type": 3, "required": False}])
    async def slash_glomp(self, ctx: SlashContext, member, *, reason=None):
        """Glomp on the specified people"""
        await functions.interactions(ctx, [member], "glomped", 'glomp', gifs.glomp, reason)

    @cog_ext.cog_slash(name="highfive", description="Highfive someone", options=[{"name": "member", "description":"The member you want to highfive.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're highfiving the member.", "type": 3, "required": False}])
    async def slash_highfive(self, ctx: SlashContext, member, *, reason=None):
        """Highfive the specified people"""
        await functions.interactions(ctx, [member], "highfived", 'hivefive', gifs.highfive, reason)

    @cog_ext.cog_slash(name="rawr", description="Rawrrrr", options=[{"name": "member", "description":"The member you want to rawr at.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're rawring at the member.", "type": 3, "required": False}])
    async def slash_rawr(self, ctx: SlashContext, member, *, reason=None):
        """Rawr at the specified people"""
        await functions.interactions(ctx, [member], "rawred at", 'rawr at', gifs.rawr, reason)

    @cog_ext.cog_slash(name="awoo", description="Howl to the moon, or someone", options=[{"name": "member", "description":"The member you want to howl at.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're howl at the member.", "type": 3, "required": False}])
    async def slash_awoo(self, ctx: SlashContext, member, *, reason=None):
        """Howl at the specified people"""
        await functions.interactions(ctx, [member], "howled at", 'howl at', gifs.awoo)

    @cog_ext.cog_slash(name="pat", description="pat someone!", options=[{"name": "member", "description":"The member you want to pat.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're patting the member.", "type": 3, "required": False}])
    async def slash_pat(self, ctx: SlashContext, member, *, reason=None):
        """Pat the specified people"""
        await functions.interactions(ctx, [member], "patted", 'pat', gifs.pet, 'pat', reason)

    @cog_ext.cog_slash(name="cookie", description="Gib cookie", options=[{"name": "member", "description":"The member you want to give a cookie to.", "type": 6, "required": True}, {"name": "reason", "description": "The reason you're giving a cookie to the member.", "type": 3, "required": False}])
    async def slash_cookie(self, ctx: SlashContext, member, *, reason=None):
        """Give cookies to the specified people"""
        await functions.interactions(ctx, [member], "gave a cookie to", 'give a cookie to', gifs.cookie, reason)

    @cog_ext.cog_slash(name="blush", description="Blushies!", options=[{"name": "member", "description":"The member you're blushing because of", "type": 6, "required": False}])
    async def slash_blush(self, ctx: SlashContext, member=None):
        """Blush (optionally because of specified people)"""
        await functions.feelings(ctx, [member] if member is not None else None, "blushes", gifs.blush)

    @cog_ext.cog_slash(name="happy",  description="Be happy", options=[{"name": "member", "description":"The member you're happy because of", "type": 6, "required": False}])
    async def slash_happy(self, ctx: SlashContext, member=None):
        """Be happy (optionally because of specified people)"""
        await functions.feelings(ctx, [member] if member is not None else None, "smiles", gifs.happy)

    @cog_ext.cog_slash(name="wag", description="wag yer tail", options=[{"name": "member", "description":"The member you're wagging your tail because of", "type": 6, "required": False}])
    async def slash_wag(self, ctx: SlashContext, member=None):
        """Wag your tail (Optionally because of specified people)"""
        await functions.feelings(ctx, [member] if member is not None else None, "wags their tail", gifs.wag)

    @cog_ext.cog_slash(name="quack", description="Quack quack!", options=[{"name": "member", "description":"The member you're quacking because of", "type": 6, "required": False}])
    async def slash_quack(self, ctx: SlashContext, member=None):
        """Quack (Optionally because of specified people)"""
        duck_list = [f"https://random-d.uk/api/{random.randint(1,191)}.jpg", f"https://random-d.uk/api/{random.randint(1,42)}.gif"]
        await functions.feelings(ctx, [member] if member is not None else None, "quacks", duck_list)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, error):
      embed = discord.Embed(title="An error has occured!", color=discord.Color.red())
      embed.add_field(name='Full Traceback', value=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\n```", inline=False)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(slash(bot))
