import discord
import random
import gifs

async def interactions(ctx, members, type, typespecial):
    GIFlist = getattr(gifs, type)
    GIF = random.choice(GIFlist)
    if not (members):
        return await ctx.send(f"Please specify at least one cutie to {type}!")
    embed = discord.Embed(color=discord.Color.green(), description=f"**{ctx.message.author.display_name}** {typespecial} " + "**" + '**, **'.join(x.display_name for x in members) + "**")
    embed.set_image(url=GIF)
    await ctx.send(embed=embed)
