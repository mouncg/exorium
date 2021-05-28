import discord
import config
import traceback
from discord.ext import commands
from discord_slash import SlashCommand


def get_prefix(bot, message):
    prefixes = ["e?"]
    
    return commands.when_mentioned_or(*prefixes)(bot, message)


#  bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True,
#  allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True, 
    allowed_mentions=discord.AllowedMentions.none(), 
    max_messages=10000,
    # intents=discord.Intents.all(),
    status=discord.Status.online,
    activity=discord.Activity(type=discord.ActivityType.playing, name=f'in the sandbox'),
    description="A bot designed to improve chatting and discord usage."
)
slash = SlashCommand(client=bot, sync_commands=True, override_type=True, sync_on_cog_reload=True)

bot.lockdown = True
bot.blacklist = {}

connection = config.connection
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (id BIGINT PRIMARY KEY, reason VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS warnings (guild_id BIGINT, user_id BIGINT, mod_id BIGINT, reason VARCHAR(255), time TIMESTAMP)")
connection.commit()

@commands.Cog.listener()
async def on_ready():
    print('Bot has started successfully.')


for extension in config.extensions:
    try:
        bot.load_extension(extension)
        print(f'[extension] {extension} was loaded successfully!')
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tbe = "".join(tb) + ""
        print(f'[WARNING] Could not load extension {extension}: {tbe}')


bot.database.execute("SELECT * FROM blacklist")
blacklist = bot.database.fetchall()
for result in blacklist:
    bot.blacklist[result['id']] = result['reason']

bot.run(config.token)
