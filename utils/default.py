import discord, random, aiohttp

def date(target, clock=True):
    if clock is False:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

async def interactions(ctx, members, name, error_name, list, reason=None, sra_url=None):
    if members is None:
        return await ctx.send(f'You must specify the user to {error_name}!')
    if sra_url is None:
        image = random.choice(list)
    else:
        api_random = random.choice(['normal', 'sra'])
        if api_random == 'normal':
            image = random.choice(list)
        elif api_random == 'sra':
            try:
                await ctx.trigger_typing()
            except AttributeError:# Slash commands can't trigger typing.
                pass
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
    if len(members) == 2:
        display_list = f"{display_list[0]} and {display_list[1]}"
    else:
        display_list = ', '.join(display_list)
    embed = discord.Embed(description=f"**{ctx.author.display_name}** {name} **" + display_list + f"**\n{'' if reason is None else f'**Reason:** {reason}'}", color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    await ctx.send(embed=embed)

async def feelings(ctx, members, name, list):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_thumbnail(url=random.choice(list))
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_list = []
        for x in members:
            display_list.append(x.display_name)
        if len(members) >= 3:
            display_list.append(f"and {display_list.pop(-1)}")
        if len(members) == 2:
            display_list = f"{display_list[0]} and {display_list[1]}"
        else:
            display_list = ', '.join(display_list)
        embed.description=f"**{ctx.author.display_name}** {name} because of **{display_list}**"
    await ctx.send(embed=embed)
