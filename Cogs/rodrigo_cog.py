import discord
from discord import *
from discord.ext import commands, tasks
from discord.ext.commands.context import Context


class RodrigoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rodrigo(self, ctx: Context, user: Member):
        self.call_rodrigo.start(ctx, user)

    @commands.command()
    async def rodrigo_rapido(self, ctx: Context, user: Member):
        self.call_rodrigo_rapido.start(ctx, user)

    @tasks.loop(hours=4)
    async def call_rodrigo(self, ctx: Context, user: Member):
        await ctx.send('<@{}> , abre o server'.format(user.id))

    @tasks.loop(minutes=20)
    async def call_rodrigo_rapido(self, ctx: Context, user: Member):
        await ctx.send('<@{}> , abre o server'.format(user.id))
