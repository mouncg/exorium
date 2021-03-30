import config
import discord
import gifs
import random
import aiohttp
import json
from discord.ext import commands

from outsources import functions


class social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Slap someone", enabled=False)
    async def slap(self, ctx, members: commands.Greedy[discord.Member]):
        """Slap the specified people"""
        if str(ctx.message.author.id) in str(members):
            await ctx.send("You can't slap yourself, derp!")
            return
        await functions.interactions(ctx, members, "slap", "slaps")
# ctx, members, type, typespecial

    @commands.command(brief="Snuggle someone")
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member]):
        """Snuggle the specified people"""
        await functions.interactions(ctx, members, "snuggle", "snuggles")

    #@commands.command(brief="Hug someone")
    #async def hug(self, ctx, members: commands.Greedy[discord.Member], *, reason="being lovely"):
    #    await functions.interactions(ctx, members, reason, "hug", "how lovely", "hugged")

    @commands.command(brief="Bonk someone", enabled=False)
    async def bonk(self, ctx, members: commands.Greedy[discord.Member]):
        """Bonk the specified people"""
        await functions.interactions(ctx, members, "bonk", "bonks")

    @commands.command(brief="Boop someone")
    async def boop(self, ctx, members: commands.Greedy[discord.Member]):
        """Boop the specified people"""
        await functions.interactions(ctx, members, "boop", "boops")
    
    @commands.command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, members: commands.Greedy[discord.Member]):
        """Smooch the specified people"""
        await functions.interactions(ctx, members, "smooch", "smooches")
        
    @commands.command(brief="Lick someone")
    async def lick(self, ctx, members: commands.Greedy[discord.Member]):
        """Lick the specified people"""
        await functions.interactions(ctx, members, "lick", "licks")
    
    @commands.command(brief="Give bellyrubs!")
    async def bellyrub(self, ctx, members: commands.Greedy[discord.Member]):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, members, "bellyrub", "gives belly rubs to")

    @commands.command(brief="Cuddle someone")
    async def cuddle(self, ctx, members: commands.Greedy[discord.Member]):
        """Cuddle the specified people"""
        await functions.interactions(ctx, members, "cuddle", "cuddles")
   
    @commands.command(brief="Feed someone")
    async def feed(self, ctx, members: commands.Greedy[discord.Member]):
        """Feed the specified people"""
        await functions.interactions(ctx, members, "feed", "feeds")

    @commands.command(brief="Glomp someone")
    async def glomp(self, ctx, members: commands.Greedy[discord.Member]):
        """Glomp on the specified people"""
        await functions.interactions(ctx, members, "glomp", "glomps on")

    @commands.command(brief="Highfive someone")
    async def highfive(self, ctx, members: commands.Greedy[discord.Member]):
        """Highfive the specified people"""
        await functions.interactions(ctx, members, "highfive", "high fives")

    @commands.command(brief="Rawrrrr")
    async def rawr(self, ctx, members: commands.Greedy[discord.Member]):
        giflist = gifs.rawr
        gif = random.choice(giflist)
        if not members:
            embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** rawrs")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** rawrs at " + "**" + '**, **'.join(x.display_name for x in members) + "**")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command(brief="Howl to the moon, or someone", aliases=["howl"])
    async def awoo(self, ctx, members: commands.Greedy[discord.Member]):
        giflist = gifs.awoo
        gif = random.choice(giflist)
        if not members:
            embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** howls")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** howls at " + "**" + '**, **'.join(x.display_name for x in members) + "**")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
        
    @commands.command(brief="Blushies!")
    async def blush(self, ctx, members: commands.Greedy[discord.Member]):
        giflist = gifs.blush
        gif = random.choice(giflist)
        if not members:
            embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** blushes")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** blushes because of " + "**" + '**, **'.join(x.display_name for x in members) + "**")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command(brief="Be happy")
    async def happy(self, ctx, members: commands.Greedy[discord.Member]):
        giflist = gifs.happy
        gif = random.choice(giflist)
        if not members:
            embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** is happy")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** Is happy because of " + "**" + '**, **'.join(x.display_name for x in members) + "**")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)
    
    @commands.command(brief="wag yer tail")
    async def wag(self, ctx, members: commands.Greedy[discord.Member]):
        giflist = gifs.wag
        gif = random.choice(giflist)
        if not members:
            embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** wags their tail")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** wags their tail because of " + "**" + '**, **'.join(x.display_name for x in members) + "**")
        embed.set_image(url=gif)
        await ctx.send(embed=embed)

    @commands.command(brief="pat someone!", aliases=["pet"])
    async def pat(self, ctx, members: commands.Greedy[discord.Member]):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                js = await r.json()
                
                if not members:
                    return await ctx.send("Please specify someone to pat.")
                e = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name} pats** " + "**" + '**,** '.join(x.display_name for x in members) + "**")
                
                manual = gifs.pet
                manual.append(js['link'])
                image = random.choice(manual)
                
                e.set_image(url=image)
                await ctx.send(embed=e)
    
    @commands.command(brief="hug someone!")
    async def hug(self, ctx, members: commands.Greedy[discord.Member]):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                js = await r.json()
                
                if not members:
                    return await ctx.send("Please specify someone to hug.")
                e = discord.Embed(color=config.color, description=f"**{ctx.message.author.display_name}** hugs " + "**" + '**, **'.join(x.display_name for x in members) + "**")
                
                manual = gifs.hug
                manual.append(js['link'])
                image = random.choice(manual)
                
                e.set_image(url=image)
                await ctx.send(embed=e)
        
    @commands.command(brief="Gib cookie")
    async def cookie(self, ctx, members: commands.Greedy[discord.Member]):
        if not members:
            return await ctx.send("Please specify at least one cutie to give a cookie to!")
        e = discord.Embed(title='A cookie has been given!', description=f'{ctx.author.mention} gave {members[0].mention} a cookie', color=config.green)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(social(bot))
