from typing import Union
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from src.natal.shuffle_amigos import ShuffleAmigos
from src.natal.amigo import Amigo
import os


class Natal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def natal(self, ctx):
        await ctx.send('Feliz Natal!')

    def get_user(self, ctx: Context,
                 user_id: str) -> Union[discord.Member, None]:
        if isinstance(ctx.guild, discord.Guild):
            return ctx.guild.get_member(int(user_id))
        return None

    @commands.command()
    async def amigo_secreto(self, ctx: Context):
        """Sorteia um amigo secreto para cada pessoa"""
        shuffle = ShuffleAmigos()
        amigos = [
            Amigo('Nicolas', '269487620629725184'),
            Amigo('Renato', '463820210328305684'),
            Amigo('Lucas', '207459010062974976'),
            Amigo('Sorriso', '439894995890208768'),
            Amigo('Cadu', '303916080152182794'),
            Amigo('Arcadia', '330365062998917130'),
            Amigo('Café', '708411791528427613'),
            Amigo('Cap', '583090254807040001'),
            Amigo('Ghost', '657739821804027924'),
            Amigo('Gukase', '763932975691333682'),
            Amigo('Eike', '381549822575902730'),
        ]
        shuffle.shuffle(amigos)
        for amigo in amigos:
            user = self.get_user(ctx, amigo.id)
            if user is None:
                await ctx.send('Usuário não encontrado')
                return

            elif amigo.amigo_secreto is not None:
                os.system(  # nosec
                    f'echo "{amigo.nome} -> {amigo.amigo_secreto.nome}" >> amigos.txt'
                )
                await user.send(
                    'Olá! Seu amigo secreto foi sorteado! De verdade dessa vez, ignore o de cima.'
                )
                await user.send(
                    f'Olá **{amigo.nome}**! Seu amigo secreto é **{amigo.amigo_secreto.nome}**!\n\n\
Qualquer forma de expressão vale, desde um desenho até mesmo um \
presente, teremos joguinhos rápidos e muita falação de bosta no \
dia, espero que se divirtam, esperamos todos no dia do amigo secreto.')
            else:
                await ctx.send('Amigo secreto não encontrado')
                return

        await ctx.send('Amigo secretos sorteados com sucesso!')

    @commands.command()
    async def send_again(self, ctx: Context):
        """Envia novamente para todos os usuários"""
        with open('amigos.txt', 'r') as file:
            for line in file:
                user_name = line.split('->')[0].strip()
                amigos = [
                    Amigo('Nicolas', '0'),
                    Amigo('Renato', '463820210328305684'),
                    Amigo('Lucas', '0'),
                    Amigo('Sorriso', '439894995890208768'),
                    Amigo('Cadu', '0'),
                    Amigo('Arcadia', '0'),
                    Amigo('Café', '0'),
                    Amigo('Cap', '0'),
                    Amigo('Ghost', '463820210328305684'),
                    Amigo('Gukase', '0'),
                    Amigo('Eike', '0'),
                ]
                user_id = next(
                    (amigo.id for amigo in amigos if amigo.nome == user_name),
                    None)
                if user_id is None:
                    await ctx.send('Usuário não encontrado')
                    continue
                user = self.get_user(ctx, user_id)
                if user is None:
                    await ctx.send('Usuário não encontrado')
                    continue
                await user.send(line)