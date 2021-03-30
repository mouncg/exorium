import discord, config, json, requests, random, aiohttp
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
        e.set_footer(text="Made using some-random-api")
        await ctx.send(embed=e)


    @commands.command(brief="Get a meme")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/meme") as r:
                js = await r.json()
                
                e = discord.Embed(color=config.color)
                e.set_author(name=js['caption'])
                e.set_image(url=js['image'])
                e.set_footer(text="Made using some-random-api")
                await ctx.send(embed=e)


    @commands.command(brief="generate random animals")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def animal(self, ctx, *args):
        delmsg = await ctx.send('Awaiting api results')
        query = ''
        for thing in args:
            query += f"{thing}+"
        if query.endswith('+'):
            query = query[:-1]
        else:
            query = "animal"
        r = requests.get(
            'https://pixabay.com/api/',
            params={'key': config.pixabaykey, 'q': query, "image_type": 'photo', 'category': 'animals'}
        )
        if r.json()["total"] == 0:
            await delmsg.delete()
            await ctx.send("Sadly, no results were found")
            return
        await delmsg.delete()
        finalimg = random.choice(r.json()["hits"])["webformatURL"]
        embed = discord.Embed(title='Random animal', color=config.color)
        embed.set_image(url=finalimg)
        embed.set_footer(text='Powered by pixabay.')
        await ctx.send(embed=embed)

    @commands.command(brief="Generate random images")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def image(self, ctx, *args):
        delmsg = await ctx.send('Awaiting api results')
        query = ''
        for thing in args:
            query += f"{thing}+"
        if query.endswith('+'):
            query = query[:-1]
        else:
            query = "animal"
        r = requests.get(
            'https://pixabay.com/api/',
            params={'key': config.pixabaykey, 'q': query, "image_type": 'photo', 'safesearch': 'true'}
        )
        if r.json()["total"] == 0:
            await delmsg.delete()
            await ctx.send("Sadly, no results were found")
            return
        await delmsg.delete()
        finalimg = random.choice(r.json()["hits"])["webformatURL"]
        embed = discord.Embed(title='Random image', color=config.color)
        embed.set_image(url=finalimg)
        embed.set_footer(text='Powered by pixabay.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(images(bot))
