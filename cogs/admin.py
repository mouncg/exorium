import config
import discord
import asyncio
import typing
from discord.ext import commands
from prettytable import PrettyTable
from utils import default
from utils.paginator import TextPages

# def admin():
#     async def predicate(ctx):
#         return ctx.author.id in ctx.bot.owner_ids
#     return commands.check(predicate)

async def suggestion_command(self, ctx, type, color, reason):
    if ctx.channel.id != 839962330787479592:
        return await ctx.send(f"{config.crossmark} You must run this command in a suggestion channel!")
    elif ctx.message.reference is None:
        return await ctx.send(f"{config.crossmark} You must reply to the message you want to approve!")

    if ctx.message.reference.cached_message is None:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    else:
        message = ctx.message.reference.cached_message
    embed = message.embeds[0]
    embed.color = color
    if reason is not None:
        embed.add_field(name=f'Reason from {ctx.author.name}', value=str(reason))
    await message.edit(embed=embed)
    user = await self.bot.try_user(int(embed.author.icon_url.split('/')[4]))
    if user is not None:
        try:
            await user.send(content=f"{ctx.author.name} just {type} your suggestion!", embed=embed)
        except:
            pass
    await ctx.send(f'{config.checkmark} {type.capitalize()} the following suggestion.')

class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "👑"
   
    @commands.group(invoke_without_command=True, aliases=['s'])
    @commands.is_owner()
    async def suggestion(self, ctx):
        """ Manage the Suggestion Queue """
        await ctx.send_help(ctx.command)

    @suggestion.command(aliases=['a'])
    @commands.is_owner()
    async def approve(self, ctx, *, reason=None):
        await suggestion_command(self, ctx, 'approved', discord.Color.green(), reason)

    @suggestion.command(aliases=['d'])
    @commands.is_owner()
    async def deny(self, ctx, *, reason=None):
        await suggestion_command(self, ctx, 'denied', discord.Color.red(), reason)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """
        Load the specified cog
        """
        self.bot.load_extension(f'cogs.{cog}')
        await ctx.send(f"{config.checkmark} loaded cog **{cog}**")
        print(f"{ctx.author} loaded cog \"{cog}\" successfully.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog='~'):
        """
        Reload a specified/all cogs
        """
        if cog == '~':
            for extension in config.extensions:
                self.bot.reload_extension(extension)
            await ctx.send(f"{config.checkmark} Reloaded all cogs successfully.")
            print(f"{ctx.author} reloaded all cogs successfully.")
        else:
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f"{config.checkmark} Reloaded cog **{cog}**")
            print(f"{ctx.author} reloaded \"{cog}\" successfully.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """
        Unload the specified cog
        """
        if cog == 'admin':
            return await ctx.send(f"{config.crossmark} Could not unload cog `admin`.")
        self.bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f"{config.checkmark} Unloaded cog **{cog}**")
        print(f"{ctx.author} unloaded \"{cog}\" Successfully.")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """ Shuts down the bot. """
        await ctx.send('Shutting down.')
        await self.bot.change_presence(activity=discord.Game(type=0, name='Shutting Down.'), status=discord.Status.dnd)
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, id):
        """
        Forcibly leave a guild through ID
        """

        def check(r, u):
            return u.id == ctx.author.id and r.message.id == checkmsg.id

        try:
            guild = await self.bot.fetch_guild(id)
        except Exception:
            return await ctx.send('This is not a discord server i\'m in.')
        e = discord.Embed(color=discord.Color.red())
        e.set_thumbnail(url=guild.icon_url)
        e.description = f"""
**Guild name:** {guild.name}
**Guild owner:** {await self.bot.fetch_user(guild.owner_id)}
**Guild owner ID:** {guild.owner_id}
Approximately **N/A** members

Created on {default.date(guild.created_at)}.
__**Are you sure you want me to leave this guild?**__
"""
        try:
            checkmsg = await ctx.send(embed=e)
            await checkmsg.add_reaction(config.checkmark)
            await checkmsg.add_reaction(config.crossmark)
            react, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)

            if str(react) == config.checkmark:
                try:
                    await checkmsg.clear_reactions()
                except Exception:
                    pass
                eleave = discord.Embed(color=discord.Color.dark_red(), description=f"Okay, leaving this guild.")
                await checkmsg.edit(embed=eleave)
                await guild.leave()
                await asyncio.sleep(3)

                log = await self.bot.get_channel(762203326519181312)

                await log.send(f"Forcibly left guild {guild}.")
                return

            if str(react) == config.crossmark:
                try:
                    await checkmsg.clear_reactions()
                except Exception:
                    pass
                estay = discord.Embed(color=discord.Color.green(), description=f"Okay, staying in this guild.")
                await checkmsg.edit(embed=estay)
                return

        except asyncio.TimeoutError:
            try:
                await checkmsg.clear_reactions()
            except Exception:
                pass
            etimeout = discord.Embed(color=discord.Color.dark_red(), description=f"Command timed out, canceling...")
            return await checkmsg.edit(embed=etimeout)

    @commands.group(aliases=["i"])
    @commands.is_owner()
    async def info(self, ctx):
        """ Display admin user/guild info """
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Info help", color=discord.Color.dark_teal())
            e.description = f"`guild` **- Guild Admin Information**\n`user` **-User Admin Information**"
            await ctx.send(embed=e)

    @info.group(aliases=["g"])
    @commands.is_owner()
    async def guild(self, ctx, *, guild: int):
        """ Guild Admin Information """

        try:
            guild = self.bot.get_guild(guild)
            owner = await self.bot.fetch_user(guild.owner_id)
        except Exception:
            return await ctx.send("Could not find this guild.")
        sperms = dict(guild.me.guild_permissions)
        perm = []

        for p in sperms.keys():
            if sperms[p] is True and guild.me.guild_permissions.administrator is False:
                perm.append(f"`{p.replace('_', ' ').title()}`")
        if guild.me.guild_permissions.administrator:
            perm.append('Administrator')

        e = discord.Embed(color=discord.Color.dark_teal())
        e.description = f"If you want me to leave this guild, use:\n`exo leave {guild.id}`"
        e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Generic information', value=f"""
**Server name:** {guild}
**Guild ID:** {guild.id}
**Owner:** {owner} ({guild.owner_id})
**{guild.member_count}** members
**{len(guild.channels)}** channels & **{len(guild.roles)}** roles total
**Created on {default.date(guild.created_at)}**
**Joined on {default.date(guild.get_member(self.bot.user.id).joined_at)}**
""")
        e.add_field(name='My permissions', value=", ".join(perm))
        await ctx.send(guild.id, embed=e)

    @info.group(aliases=["u"])
    @commands.is_owner()
    async def user(self, ctx, *, user: typing.Union[discord.User, str]):
        """ User Admin Information """
        try:
            e = discord.Embed(color=discord.Color.dark_teal())
            e.set_author(name=user, icon_url=user.avatar_url)
            e.set_thumbnail(url=user.avatar_url)
            e.description = f"""
**User profile:** [{user}](https://discord.com/users/{user.id})
**Avatar URL:** [Click here]({user.avatar_url})
**Created on {default.date(user.created_at)}**
**Public Flags value:** {user.public_flags.value}
**{len([x for x in self.bot.guilds if x.get_member(user.id)])}** mutual servers
"""
            await ctx.send(embed=e)
        except Exception:
            return await ctx.send(f'**I could not find {user} as user.**')

#########################################
########################################
    @commands.group(name='blacklist', invoke_without_command=True)  # invoke_without_command means you can have separate permissions/cooldowns for each subcommand
    @commands.is_owner()
    async def blacklist(self, ctx):
        await ctx.send_help(ctx.command)

    @blacklist.command(name='user')
    @commands.is_owner()
    async def blacklist_user(self, ctx, user: typing.Union[discord.User, int], *, reason: str = 'No reason provided'):
        """ Blacklist or unblacklist a user """
        try:
            if isinstance(user, discord.User):
                pass
            elif isinstance(user, int):
                user = await self.bot.fetch_user(user)
        except Exception as e:
            return await ctx.send(f"Failed to find the user: `{e}`")

        try:
            self.bot.blacklist[user.id]
            await self.bot.database.execute("DELETE FROM blacklist WHERE id = $1", user.id)
            self.bot.blacklist.pop(user.id)
            await ctx.send(f"unblacklisted {user}")          
        except Exception:
            await self.bot.database.execute("INSERT INTO blacklist VALUES($1, $2)", user.id, reason)
            self.bot.blacklist[user.id] = reason
            bluser = await self.bot.fetch_user(user.id)
            e = discord.Embed(title=f"{user.name} ({user.id}) blacklisted", color=discord.Color.dark_red())
            e.description = f"Your account has been blacklisted by an administrator or developer at Esquire. If you wish to know why, you can join the [support server]({config.support}). Please however note that no one is obligated to explain to you why your account was blacklisted. Please also check [our terms of use](https://glenntwebs.github.io/esqweb/legal.html) here."
            e.set_thumbnail(url=self.bot.user.avatar_url)
            try:
                await bluser.send(embed=e)
            except discord.Forbidden:
                pass
            await ctx.send(f"blacklisted {user}")

    @blacklist.command(name='server')
    @commands.is_owner()
    async def blacklist_server(self, ctx, server: int, *, reason: str = 'No reason provided'):
        """ Blacklist or unblacklist a server """
        try:
            self.bot.blacklist[server]
            await self.bot.database.execute("DELETE FROM blacklist WHERE id = $1", server)
            self.bot.blacklist.pop(server)
            await ctx.send(f"unblacklisted {server}")          
        except Exception:
            await self.bot.database.execute("INSERT INTO blacklist(id, reason) VALUES($1, $2)", server, reason)
            self.bot.blacklist[server] = reason
            guild = self.bot.get_guild(server)
            if guild:

                owner = await self.bot.fetch_user(guild.owner_id)
                e = discord.Embed(title=f"{guild.name} ({guild.id}) blacklisted", color=discord.Color.dark_red())
                e.description = f"Your server has been blacklisted by an administrator or developer at Esquire. If you wish to know why, you can join the [support server]({config.support}). Please however note that no one is obligated to explain to you why your server was blacklisted. Please also check [our terms of use](https://glenntwebs.github.io/esqweb/legal.html) here."
                e.set_thumbnail(url=self.bot.user.avatar_url)
                try:
                    await owner.send(embed=e)
                except discord.Forbidden:
                    pass
                await guild.leave()
            await ctx.send(f"blacklisted {server}")

    @commands.command()
    @commands.is_owner()
    async def ownertest(self, ctx):
        await ctx.send(_("Hello!"))

    @commands.command(name="sql")
    @commands.is_owner()
    async def sql(self, ctx, *, query):
        """ Execute psql query """
        try:
            if query.__contains__('guild.id'):
                query = query.replace('guild.id', str(ctx.guild.id))
            if query.__contains__('author.id'):
                query = query.replace('author.id', str(ctx.author.id))
            if query.__contains__('channel.id'):
                query = query.replace('channel.id', str(ctx.channel.id))

            if not query.lower().startswith("select"):
                data = await self.bot.database.execute(query)
                return await ctx.send(data)

            data = await self.bot.database.fetch(query)
            if not data:
                return await ctx.send("Table seems to be empty!")
            columns = []
            values = []
            for k in data[0].keys():
                columns.append(k)

            for y in data:
                rows = []
                for v in y.values():
                    rows.append(v)
                values.append(rows)

            x = PrettyTable(columns)
            for d in values:
                x.add_row(d)

            pages = TextPages(ctx,
                              text=f'\n{x}')
            return await pages.paginate()
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Admin(bot))
