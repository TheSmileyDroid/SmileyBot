import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context


class DefaultCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected as {}'.format(self.bot.user.display_name))

    @commands.command()
    async def test(self, ctx: Context, args: str):
        await ctx.send(args)
