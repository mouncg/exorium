import discord

token = 'BOT_TOKEN'

extensions = ['jishaku',
              'cogs.help',
              'cogs.events.error',
              'cogs.events.logs',
              #'cogs.events.statcord', # Fix statcord posting when Statcord self is fixed
              'cogs.social',
              'cogs.admin',
              'cogs.DLP',
              'cogs.social_slash',
              'cogs.mod']

invite = "https://discord.com/api/oauth2/authorize?client_id=620990340630970425&permissions=335932630&scope=bot"
invite2 = "https://discord.com/oauth2/authorize?client_id=764129783965286414&scope=bot&permissions=8"
privacy = "https://flitzstudios.github.io/exoriumbot/src/pages/legal.html"
support = "https://discord.gg/CEHkNky"

# In case of selfhosting, you will need to edit the used emotes.
checkmark = "<a:checkmark:813798012399779841>"
crossmark = "<a:cross:813798012626141185>"
confused = "<a:confused:837702171747024896>"
inv = '<:inv:833995767055515678>'


DELTOKEN = "Token from DiscordExtremeList"
TOPTOKEN = "Top.gg Token"
DBLTOKEN = "DiscordBotlist.com token"
STATTOKEN = "statcord.com token"
GENIUSTOKEN = "genius.com token"