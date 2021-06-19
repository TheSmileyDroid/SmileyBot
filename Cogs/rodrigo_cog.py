import discord
from discord import *
from discord.ext import commands, tasks
from discord.ext.commands.context import Context


class RodrigoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rodrigo(self, ctx: Context):
        self.call_rodrigo.start(ctx)

    @tasks.loop(hours=4)
    async def call_rodrigo(self, ctx):
        await ctx.send('Rodrigo, abre o server')
