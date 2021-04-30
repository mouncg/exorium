import discord
import aiohttp
from discord.ext import commands


def admin():
    async def predicate(ctx):
        administrators = ctx.author.id == 809057677716094997 or ctx.author.id == 345457928972533773 or ctx.author.id == 443217277580738571 or ctx.author.id == 699686304388087858
        if not administrators:
            raise admin_only()
        else:
            return administrators
    return commands.check(predicate)

class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(discord.Object(id=member_id))
            except discord.NotFound:
                raise commands.BadArgument('This member has not been banned before.') from None

        elif not argument.isdigit():
            ban_list = await ctx.guild.bans()
            entity = discord.utils.find(lambda u: str(u.user.name) == argument, ban_list)
            if entity is None:
                raise commands.BadArgument('This member has not been banned before.')
            return entity


class admin_only(commands.CheckFailure):
    pass