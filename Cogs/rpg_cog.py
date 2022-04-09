# RPG Cog

from unittest import result
import discord
from discord.ext import commands

import random
import os


class RPG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['r', 'dado', 'd'])
    async def roll(self, ctx, *, args):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = args.split('d')
        except:
            await ctx.send('O formato deve ser NdN!')
            return
        try:
            rolls = int(rolls)
            limit = int(limit)
        except:
            await ctx.send('O formato deve ser NdN!')
            return

        numbers = [str(random.randint(1, limit)) for r in range(rolls)]
        result = ((', '.join(numbers) + ' = ') if len(numbers) > 1 else
                  '') + str(sum(int(n) for n in numbers))
        await ctx.send(result)

    @commands.command()
    async def flip(self, ctx, *, args):
        """Flips a coin."""
        await ctx.send(random.choice(['Cara', 'Coroa']))

    @commands.command()
    async def escolher(self, ctx, *, args):
        """Chooses between multiple options."""
        choices = args.split(' ou ')
        await ctx.send(random.choice(choices))

    @commands.command()
    async def ficha(self, ctx, *, args):
        """Creates a character sheet."""
        await ctx.send('A ficha não está disponível no momento.')