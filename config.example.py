import discord
import mysql.connector

# The bot token, which defines what bot to start
token = 'bot token'

# This loads the cogs.
extensions = ['jishaku', # Jishaku is an extension we use for debugging and testing (https://github.com/Gorialis/jishaku)
              'cogs.help',
              'cogs.events.error',
              'cogs.events.logs',
              #'cogs.events.statcord', # Fix statcord posting when Statcord self is fixed
              'cogs.social',
              'cogs.admin',
              'cogs.DLP',
              'cogs.social_slash',
              'cogs.mod']

# links related to the bot (invite2 is a admin invite link with permission integer 8)
invite = ""
invite2 = ""
privacy = ""
support = ""

# emotes
checkmark = ""
crossmark = ""
confused = ""
inv = ""

# The tokens for APIs
DELTOKEN = ""
TOPTOKEN = ""
DBLTOKEN = ""
STATTOKEN = ""
GENIUSTOKEN = ""

# Connect to the database
DB_CONN_INFO = {
    "user": "",
    "password": "",
    "host": "",
    "database": ""
}
