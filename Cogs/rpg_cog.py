# RPG Cog
from discord.ext import commands
import random


class RPG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['r', 'dado', 'd'])
    async def roll(self, ctx, *, args: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit_modifier = args.split('d')
            limit, modifier = limit_modifier.split(['+ -'])
        except Exception as e:
            await ctx.send(f'O formato deve ser NdN! Error: {e}')
            return
        try:
            rolls = int(rolls)
            limit = int(limit)
            modifier = int(modifier)
        except Exception as e:
            await ctx.send(f'O formato deve ser NdN! Error: {e}')
            return

        numbers = [str(random.randint(1, limit)) for r in range(rolls)]
        result = ((', '.join(numbers) + ' = ') if len(numbers) > 1 else
                  '') + str(sum(int(n) for n in numbers)+modifier)
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
    async def ficha(self, ctx):
        """Shows your character sheet."""
        await ctx.send('')
