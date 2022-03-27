from discord import Member, VoiceChannel
from discord.ext import commands
from discord.ext.commands.context import Context


class Basic(commands.Cog):
    '''Usado para testes'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect_to_voice(self, ctx: Context):
        '''Conecta o bot a um canal de voz'''
        if isinstance(ctx.author, Member):
            autor: Member = ctx.author
            await autor.voice.channel.connect()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Connected as {self.bot.user.display_name}')

    @commands.command()
    async def test(self, ctx: Context, args: str):
        await ctx.send(args)

    @commands.command()
    async def move(self, _ctx: Context, user: Member, channel: VoiceChannel):
        await user.edit(voice_channel=channel)

    @commands.command()
    async def list_voice_channels(self, ctx: Context):
        await ctx.send()

    @commands.command()
    async def stay_awake(self, ctx: Context, half: int):
        '''Esse comando serve para manter o bot acordado por um tempo (em meia horas)'''

        # For each half hour in the half variable, a request will be sent to the link https://smiley-droid-bot.herokuapp.com/
        import requests
        import threading
        from time import sleep

        requests.get('https://smiley-droid-bot.herokuapp.com/', timeout=1000)

        def keep_alive():
            for i in range(half):
                # Sleep for 25 minutes
                sleep(60 * 25)
                requests.get('https://smiley-droid-bot.herokuapp.com/',
                             timeout=1000)

        thread = threading.Thread(target=keep_alive)
        thread.start()