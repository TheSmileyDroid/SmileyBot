import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context
import sqlite3 as sq

# con = sq.connect('cassino.db')
# cur = con.cursor()

# con.commit()
# con.close()


class CassinoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        con = sq.connect('cassino.db')
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS jogadores(id integer, dinheiro real)')
        con.commit()
        con.close()

    @commands.command()
    async def start(self, ctx: Context):
        con = sq.connect('cassino.db')
        cur = con.cursor()
        cur.execute('INSERT OR IGNORE INTO jogadores VALUES (?,?)',
                    (ctx.author.id, 1000))
        con.commit()
        con.close()
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
        con = sq.connect('cassino.db')
        cur = con.cursor()
        if dinheiro1 - qtd < 0:
            con.close()
            await ctx.send("{} você só tem R${:.2f}".format(ctx.author.display_name, dinheiro1))
            return
        cur.execute("UPDATE jogadores SET dinheiro=? WHERE id=?",
                    (dinheiro1-qtd, ctx.author.id))
        cur.execute("UPDATE jogadores SET dinheiro=? WHERE id=?",
                    (dinheiro2+qtd, member.id))
        await ctx.send("{}: R${:.2f}\n{}: R${:.2f}".format(ctx.author.display_name, dinheiro1 - qtd, member.display_name, dinheiro2+qtd))
        con.commit()
        con.close()

def get_dinheiro(id: int):
    con = sq.connect('cassino.db')
    cur = con.cursor()
    cur.execute("""
        SELECT dinheiro FROM jogadores WHERE id=?
    """, [id])
    dinheiro = cur.fetchone()
    con.close()
    return dinheiro[0]
