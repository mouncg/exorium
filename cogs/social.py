import config
import discord
import gifs
import random
import aiohttp
import json
from discord.ext import commands
from utils import default as functions
from utils.paginator import Pages


class social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "<:hug:642196733706764288>"

    @commands.command(brief="Slap someone", enabled=False)
    async def slap(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Slap the specified people"""
        if str(ctx.author.id) in str(members):
            return await ctx.send("You can't slap yourself, derp!")
        await functions.interactions(ctx, members, "slapped", 'slap', gifs.slap, reason)

    @commands.command(brief="Snuggle someone")
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Snuggle the specified people"""
        await functions.interactions(ctx, members, "snuggled", 'snuggle', gifs.snuggle, reason)

    @commands.command(brief="Hug someone")
    async def hug(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
       await functions.interactions(ctx, members, "hugged", 'hug', gifs.hug, reason, 'hug')

    @commands.command(brief="Bonk someone", enabled=False)
    async def bonk(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Bonk the specified people"""
        await functions.interactions(ctx, members, "bonked", 'bonk', gifs.bonk, reason)

    @commands.command(brief="Boop someone")
    async def boop(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Boop the specified people"""
        await functions.interactions(ctx, members, "booped", 'boop', gifs.boop, reason)

    @commands.command(brief="Smooch someone", aliases=["kiss"])
    async def smooch(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Smooch the specified people"""
        await functions.interactions(ctx, members, "smooched", 'smooch', gifs.smooch, reason)

    @commands.command(brief="Lick someone")
    async def lick(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Lick the specified people"""
        await functions.interactions(ctx, members, "licked", 'lick', gifs.lick, reason)

    @commands.command(brief="Give bellyrubs!")
    async def bellyrub(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, members, "bellyrubbed", 'rub the belly of', gifs.bellyrub, reason)
   
    @commands.command(brief="Nuzzle someone")
    async def nuzzle(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Nuzzle the specified people"""
        await functions.interactions(ctx, members, "nuzzled", 'nuzzles', gifs.nuzzle, reason)
    
    @commands.command(brief="Cuddle someone")
    async def cuddle(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Cuddle the specified people"""
        await functions.interactions(ctx, members, "cuddled", 'cuddle', gifs.cuddle, reason)

    @commands.command(brief="Feed someone")
    async def feed(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Feed the specified people"""
        await functions.interactions(ctx, members, "fed", 'feed', gifs.feed, reason)

    @commands.command(brief="Glomp someone")
    async def glomp(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Glomp on the specified people"""
        await functions.interactions(ctx, members, "glomped", 'glomp', gifs.glomp, reason)

    @commands.command(brief="Highfive someone")
    async def highfive(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Highfive the specified people"""
        await functions.interactions(ctx, members, "highfived", 'hivefive', gifs.highfive, reason)

    @commands.command(brief="Rawrrrr")
    async def rawr(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Rawr at the specified people"""
        await functions.interactions(ctx, members, "rawred at", 'rawr at', gifs.rawr, reason)

    @commands.command(brief="Howl to the moon, or someone", aliases=["howl"])
    async def awoo(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Howl at the specified people"""
        await functions.interactions(ctx, members, "howled at", 'howl at', gifs.awoo)

    @commands.command(brief="pat someone!", aliases=["pet"])
    async def pat(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Pat the specified people"""
        await functions.interactions(ctx, members, "patted", 'pat', gifs.pet, 'pat', reason)

    @commands.command(brief="Gib cookie")
    async def cookie(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason=None):
        """Give cookies to the specified people"""
        await functions.interactions(ctx, members, "gave a cookie to", 'give a cookie to', gifs.cookie, reason)

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
        
    @commands.command(brief="Quack quack!")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def quack(self, ctx, members: commands.Greedy[discord.Member] = None):
        """Quack (Optionally because of specified people)"""
        duck_list = [f"https://random-d.uk/api/{random.randint(1,191)}.jpg", f"https://random-d.uk/api/{random.randint(1,42)}.gif"]
        await functions.feelings(ctx, members, "quacks", duck_list)

    @commands.command(brief="random animal fact")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get animal facts! """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/dog") as r:
                async with cs.get("https://some-random-api.ml/facts/cat") as c:
                    async with cs.get("https://some-random-api.ml/facts/panda") as p:
                        async with cs.get("https://some-random-api.ml/facts/fox") as f:
                            async with cs.get("https://some-random-api.ml/facts/bird") as b:
                                async with cs.get("https://some-random-api.ml/facts/koala") as k:
                                    facts = [r, c, p, f, b, k]
                                    rc = random.choice(facts)
                                    js = await rc.json()

                                    await ctx.send(js['fact'])

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                js = await r.json()

                e = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
                e.set_image(url=js['image'])
                await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None):
        """ Gay overlay on avatar """
        if not user:
            user = ctx.author
        link = f"https://some-random-api.ml/canvas/gay/?avatar={user.avatar_url}"
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=link)
        e.set_footer(text=f"Gay avatar: {user}")
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lyrics(self, ctx, *, title):
        """ Get song lyrics """
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/lyrics?title={title}") as r:
                js = await r.json()
                
                lyricsArray = js['lyrics'].split("\n")
                
                paginator = Pages(self.context,
                          title="[{0}]({1}) by {2}".format(js['title'], js['links']['genius'], js['author']),
                          entries=lyricsArray,
                          thumbnail=js['thumbnail']['genius'],
                          per_page=15,
                          embed_color=discord.Color.dark_teal(),
                          show_entry_count=True)
                await paginator.paginate()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pokemon(self, ctx, pokemon):
        """ Get pokemon info """
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}") as r:
                    js = await r.json()


                async with cs.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon}") as t:
                    js1 = await t.json()



                abilities = []
                for x in js['abilities']:
                    abilities.append(f"[{x['ability']['name'].replace('-', ' ').capitalize()}]({x['ability']['url']})")


                type = []
                for x in js['types']:
                    type.append(f"[{x['type']['name'].replace('-', ' ').capitalize()}]({x['type']['url']})")

                e = discord.Embed(color=discord.Color.dark_teal())
                #e.set_author(name=js['caption'])
                e.title = js['name'].capitalize() + f" Evo. stage {js1['family']['evolutionStage']}"
                e.description = f"""
*Read everything on [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{pokemon}_(Pok%C3%A9mon))*

**Abilities:** {", ".join(abilities)}
**Type:** {", ".join(type)}

**Description:** {js1['description']}
**Evolution:** {' - '.join(js1['family']['evolutionLine'])}
**Egg groups:** {', '.join(js1['egg_groups'])}
**Species:** {', '.join(js1['species'])}
"""
                st = js1['stats']
                e.set_thumbnail(url=js['sprites']['other']['official-artwork']['front_default'])
                e.add_field(name="Statistics",
                            value=f"**{st['hp']}** HP\n" \
                                  f"**{st['attack']}** Attack\n" \
                                  f"**{st['defense']}** Defense\n" \
                                  f"**{st['sp_atk']}** Special Attack\n" \
                                  f"**{st['sp_def']}** Special Defense\n" \
                                  f"**{st['speed']}** Speed")
                #e.set_footer(text="Made using some-random-api")
                await ctx.send(embed=e)
        except Exception:
            return await ctx.send(f"{config.confused} **Please provide an existent pokemon. If you did, the API might be down.**")


def setup(bot):
    bot.add_cog(social(bot))
