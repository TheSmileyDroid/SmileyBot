# RPG Cog
from discord.ext import commands
import random
import re

random.seed()

class RPG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['r', 'dado', 'd'])
    async def roll(self, ctx, *, args: str):
        """Rolls a dice in NdN+N format."""
        args = args.replace(' ', '')
        dice = re.findall(r'(\d+)d(\d+)([+-]\d+)?', args)
        dice = [int(dice[0][0]), int(dice[0][1]), int(dice[0][2]) if dice[0][2] else 0]
        if len(dice) == 0:
            await ctx.send('Formato inválido. Exemplo: 3d6+1')
            return
        try:
            rolls = int(dice[0])
            limit = int(dice[1])
            modifier = int(dice[2]) if dice[2] else 0
        except Exception as e:
            await ctx.send(f'O formato deve ser NdN+N! Error when converting: {e}\
                \ndice: {dice}')
            return

        numbers = [str(random.randint(1, limit)) for r in range(rolls)]
        result = ((', '.join(numbers) if modifier else None) + ' = ' + str(sum(int(n) for n in numbers) + modifier)) if len(numbers) > 1 else '' + str(sum(int(n) for n in numbers) + modifier)
        result += f' ({str(sum(int(n) for n in numbers))} _**{modifier:+}**_)' if modifier else ''
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
