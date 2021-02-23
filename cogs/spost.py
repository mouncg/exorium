import json, requests, aiohttp, asyncio

class spost(commands.Cog, name="Server post"):
    def __init__(self, bot):
        self.bot = bot

async def api():
    while True:
        if bot.is_ready() is False:
            await asyncio.sleep(5)
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api.discordextremelist.xyz/v2/bot/{bot.user.id}/stats",
                                    headers={'Authorization': config.DELTOKEN, "Content-Type": 'application/json'},
                                    data=json.dumps({'guildCount': len(bot.guilds)})) as r:
                js = await r.json()
                if js['error']:
                    print(f'Failed to post to discordextremelist.xyz\n{js}')
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://discordbotlist.com/api/v1/bots/{bot.user.id}/stats",
                                    headers={'Authorization': config.DBLTOKEN, "Content-Type": 'application/json'},
                                    data=json.dumps({'guilds': len(bot.guilds), 'users': len(bot.users)})) as r2:
                if not r2.status == 200:
                    print(f'Failed to post to discordbotlist.com')
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://top.gg/api/bots/{bot.user.id}/stats",
                                    headers={'Authorization': config.TOPTOKEN, "Content-Type": 'application/json'},
                                    data=json.dumps({'server_count': len(bot.guilds)})) as r3:
                if not r3.status == 200:
                    print(f'Failed to post to top.gg')
                activity = discord.Game(name=f'exo help | {len(bot.guilds)} guilds', type=1)
                await bot.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(300)
bot.loop.create_task(api())

def setup(bot):
    bot.add_cog(spost(bot))
