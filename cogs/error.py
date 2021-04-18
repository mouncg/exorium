import asyncio
import discord
import traceback
from discord.ext import commands


class error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            embed = discord.Embed(description=str(error), color=discord.Color.red())
            msg = await ctx.send(embed=embed)
            if ctx.author.id in self.bot.owner_ids:
                await msg.add_reaction('\U0000203c')

                def react_check(reaction, user):
                    if ctx.author.id == user.id and reaction.emoji == '\U0000203c' and reaction.message.id == msg.id:
                        return True
                    return False

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=react_check)
                except asyncio.TimeoutError:
                    try:
                        await msg.remove_reaction('\U0000203c', self.bot.user)
                    except:
                        pass
                embed2 = discord.Embed(
                    description=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\n```",
                    color=discord.Color.red())
                await ctx.send(embed=embed2)
                try:
                    await msg.clear_reactions()
                except:
                    pass


def setup(bot):
    bot.add_cog(error(bot))
