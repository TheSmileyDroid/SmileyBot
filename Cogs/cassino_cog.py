from datetime import datetime, time, timedelta
import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context
from tinydb import TinyDB, Query
import random

db = TinyDB('./cassino.json')

timestr = '%Y-%m-%d %H:%M'

pedidos = []


class CassinoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx: Context):
        if get_jogador(ctx.author.id) != None:
            await ctx.send("Você já está no cassino e não tem como sair dele")
            return
        db.insert({'id': ctx.author.id, 'dinheiro': 1000,
                  'last_time': str(0)})
        await ctx.send("Parabéns {}! Você entrou no cassinão do sorriso! Você começa com R$1000.00".format(ctx.author.display_name))

    @commands.command()
    async def info(self, ctx: Context, member: discord.Member = None):
        try:
            if member == None:
                dinheiro = get_dinheiro(ctx.author.id)
                await ctx.send("{}: \nDinheiro: R${:.2f}".format(ctx.author.display_name, dinheiro))
            else:
                dinheiro = get_dinheiro(member.id)
                await ctx.send("{}: \nDinheiro: R${:.2f}".format(member.display_name, dinheiro))
        except TypeError:
            await ctx.send("Essa pessoa não participa do cassino")

    @commands.command()
    async def give(self, ctx: Context, member: discord.Member, qtd: int):
        dinheiro1 = get_dinheiro(ctx.author.id)
        dinheiro2 = get_dinheiro(member.id)

        if dinheiro1 - qtd < 0:
            await ctx.send("{} você só tem R${:.2f}".format(ctx.author.display_name, dinheiro1))
            return
        add_dinheiro(ctx.author.id, -qtd)
        add_dinheiro(member.id, qtd)
        await ctx.send("{}: R${:.2f}\n{}: R${:.2f}".format(ctx.author.display_name, dinheiro1 - qtd, member.display_name, dinheiro2+qtd))

    @commands.command()
    async def day(self, ctx: Context):
        if get_jogador(ctx.author.id).get('last_time') != None:
            if get_jogador(ctx.author.id).get('last_time') != str(datetime.now().day):
                dinheiro = get_dinheiro(ctx.author.id)
                qtd = random.randint(10, 100)
                add_dinheiro(ctx.author.id, qtd)
                await ctx.send("Recompensa diaria: R${} (R${})".format(qtd, dinheiro + qtd))
                jogadores = Query()
                db.update({'last_time': str(datetime.now().day)},
                          jogadores.id == ctx.author.id)
                return
            await ctx.send("Você tem que esperar 1 dia")

    @commands.command()
    async def moeda(self, ctx: Context, member: Member, qtd: int):
        pedidos.append((ctx.author, member, qtd))
        await ctx.send("<@{}> você aceita o desafio? %y/%n".format(member.id))

    @commands.command()
    async def y(self, ctx: Context):
        for pedido in pedidos:
            if pedido[1] == ctx.author:
                n = random.randint(0, 1)
                if n == 0:
                    add_dinheiro(pedido[1].id, -pedido[2])
                    add_dinheiro(pedido[0].id, pedido[2])
                    await ctx.send("<@{}> você ganhou!".format(pedido[n].id))
                    pedidos.remove(pedido)
                elif n == 1:
                    add_dinheiro(pedido[0].id, -pedido[2])
                    add_dinheiro(pedido[1].id, pedido[2])
                    await ctx.send("<@{}> você ganhou!".format(pedido[n].id))
                    pedidos.remove(pedido)

    async def n(self, ctx: Context):
        for pedido in pedidos:
            if pedido[1] == ctx.author:
                pedidos.remove(pedido)
                await ctx.send("Aposta cancelada")


def get_jogador(id):
    jogadores = Query()
    try:
        return db.search(jogadores.id == id)[0]
    except:
        return None


def add_dinheiro(id, qtd):
    if get_jogador(id) != None:
        jogadores = Query()
        db.update({'dinheiro': get_dinheiro(id)+qtd}, jogadores.id == id)


def get_dinheiro(id: int):
    jogadores = Query()
    return db.search(jogadores.id == id)[0]['dinheiro']
