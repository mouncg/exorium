import discord
import asyncio
import config
import traceback
import datetime
import asyncpg

from discord.ext import commands
from discord_slash import SlashCommand


def get_prefix(bot, message):
    prefixes = ["e?"]
    
    return commands.when_mentioned_or(*prefixes)(bot, message)


async def run():
    db = await asyncpg.create_pool(**config.DB_CONN_INFO)

    bot = Bot(database=db)
    bot.loop = asyncio.get_event_loop()
    slash = SlashCommand(client=bot, sync_commands=True, override_type=True, sync_on_cog_reload=True)

    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.now()
    try:
        await db.execute('CREATE TABLE IF NOT EXISTS blacklist (id BIGINT PRIMARY KEY, reason TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS warnings (guild_id BIGINT, user_id BIGINT, mod_id BIGINT, reason TEXT, time TIMESTAMP)')
        res = await db.fetch('SELECT * FROM blacklist')
        for the_id in red:
            bot.blacklist[the_id['id']] = the_id['reason']
            print("Loaded blacklist")

        await bot.start(config.token)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.playing, name='in the sandbox'),
            reconnect=True,
            allowed_mentions=discord.AllowedMentions.none(),
            max_messages=10000,
            intents=discord.Intents.default()
        )

        for extension in config.extensions:
            try:
                self.load_extension(extension)
                print(f'[extension] {extension} was loaded successfully!')
            except Exception as e:
                tb = traceback.format_exception(type(e), e, e.__traceback__)
                tbe = "".join(tb) + ""
                print(f'[WARNING] Could not load extension {extension}: {tbe}')

        self.database = kwargs.pop('database', None)
        self.lockdown = True
        self.blacklist = {}
    
    async def on_ready(self):
        print('Bot has started successfully.')


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
