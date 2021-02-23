import discord, config
from discord.ext import commands
from utils.checks import BannedMember

class mod(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Ban someone")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True, manage_messages=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            if member == ctx.message.author:
                return await ctx.send("You can not ban yourself, please try someone else.")
            botmember = ctx.guild.me
            if member.top_role > botmember.top_role:
                return await ctx.send("My role is too low in the hierarchy. Please move it above the highest role the user you are trying to ban has.")
            await ctx.message.delete()
            messageok = f"You were banned from `{ctx.guild.name}` with reason:\n\n{reason}"
            await member.send(messageok)
            await member.ban(reason=f"Moderator: {ctx.message.author} | Reason: {reason}")
            e = discord.Embed(title=f"{member} was banned | {reason}", color=config.red)
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(f"```py\n{e}\n```")

    @commands.command(brief="Unban someone from the server")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True, manage_messages=True)
    async def unban(self, ctx, user: BannedMember, *, reason="No reason provided"):
        try:
            await ctx.message.delete()
            await ctx.guild.unban(user.user, reason=f"moderator: {ctx.message.author} | {reason}")
            await ctx.send(f"**{user}** was unbanned successfully, with reason: ``{reason}``", delete_after=15)
        except Exception as e:
            await ctx.send(f"```py\n{e}\n```")

    @commands.command(brief="Ban and immediately unban someone")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True, manage_messages=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            if member == ctx.message.author:
                return await ctx.send("You can not softban yourself, please try someone else.")
            botmember = ctx.guild.me
            if member.top_role > botmember.top_role: 
                return await ctx.send("My role is too low in the hierarchy. Please move it above the highest role the user you are trying to ban has.")
            await ctx.message.delete()
            messageok = f"You were softbanned from `{ctx.guild.name}` with reason:\n\n{reason}"
            await member.send(messageok)
            await member.ban(reason=f"Moderator {ctx.message.author} | Reason: {reason}")
            await ctx.guild.unban(member, reason=f"moderator: {ctx.message.author} | softban")
            e = discord.Embed(title=f"{member} was softbanned | {reason}", color=config.red)
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(f"```py\n{e}\n```")
    
    @commands.command(brief="Kick someone from the server")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            if member == ctx.message.author:
                return await ctx.send("You can not kick yourself, please try someone else.")
            botmember = ctx.guild.me
            if member.top_role > botmember.top_role:
                return await ctx.send("My role is too low in the hierarchy. Please move it above the highest role the user you are trying to ban has.")
            await ctx.message.delete()
            messageok = f"You've been kicked from __**{ctx.guild.name}**__ with reason:\n\n{reason}"
            await member.send(messageok)
            await member.kick(reason=f"Moderator {ctx.message.author} | Reason: {reason}")
            e = discord.Embed(title=f"{member} was softbanned | {reason}", color=config.red)
            await ctx.send(embed=e)
        except Exception as e:
            await ctx.send(f"```py\n{e}\n```")
        
def setup(bot):
    bot.add_cog(mod(bot))
