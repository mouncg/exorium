import discord, random, aiohttp

def date(target, clock=True):
    if clock is False:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

async def interactions(ctx, members, name, list, reason=None, sra_url=None):
    if sra_url is None:
        image = random.choice(list)
    else:
        api_random = random.choice(['normal', 'sra'])
        if api_random == 'normal':
            image = random.choice(list)
        elif api_random == 'sra':
            await ctx.trigger_typing()
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://some-random-api.ml/animu/{sra_url}') as r:
                    if r.status == 200:
                        js = await r.json()
                        image = js['link']
                    else:
                        image = random.choice(list)
    display_list = []
    for x in members:
        display_list.append(x.display_name)
    if len(members) >= 3:
        display_list.append(f"and {display_list.pop(-1)}")
    embed = discord.Embed(description=f"**{ctx.author.display_name}** {name} **" + ', '.join(display_list) + f"**\n{'' if reason is None else f'**Reason:** {reason}'}", color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    await ctx.send(embed=embed)

async def feelings(ctx, members, name, list):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_list = []
        for x in members:
            display_list.append(x.display_name)
        if len(members) >= 3:
            display_list.append(f"and {display_list.pop(-1)}")
        embed.description=f"**{ctx.author.display_name}** {name} because of {display_list}"
    await ctx.send(embed=embed)
