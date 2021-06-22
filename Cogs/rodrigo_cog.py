import discord
from discord import *
from discord.ext import commands, tasks
from discord.ext.commands.context import Context
import sqlite3

class RodrigoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        connection = sqlite3.connect("rodrigo.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Sub (name TEXT, channel TEXT, member TEXT)")
        connection.close()
        self.call_rodrigo.start()

    @commands.command()
    async def rodrigo(self, ctx: Context, user: Member):
        connection = sqlite3.connect("rodrigo.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Sub VALUES (?,?,?)", (ctx.channel.name, ctx.channel.id, user.id))
        connection.commit()
        connection.close()
        self.call_rodrigo.stop()
        self.call_rodrigo.start()
        


    @tasks.loop(hours=4)
    async def call_rodrigo(self):
        connection = sqlite3.connect("rodrigo.db")
        cursor = connection.cursor()
        for result in cursor.execute('SELECT * FROM Sub'):
          await (discord.utils.get(self.bot.get_all_channels(), id=result[1])).send('<@{}> , abre o server'.format(result[2]))
        connection.close()

