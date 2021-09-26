import asyncio
from re import L
from gtts.tts import gTTS
from utils import get_voice_channel_and_status, get_voice_client, voice_clients
import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, ctx=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


loop = False
players = []
current = []

class TocarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def next_music(self, ctx: Context):
        global loop
        global current
        if not loop:
            def err(e):
                print('Player error: %s' % e) if e else None
                self.next_music(ctx)
            if len(players) > 0:
                c = players.pop(0)
                ctx.voice_client.play(c, after=err)
                current[0] = c
        else:
            def err(e):
                print('Player error: %s' % e) if e else None
                self.next_music(ctx)
            ctx.voice_client.play(current[0], after=err)
            
    
    @commands.command()
    async def queue(self, ctx: Context):
        text = ''
        for player in players:
            text += '{}\n'.format(player.title)
        await ctx.send(text)

    @commands.command()
    async def play(self, ctx: Context, url: str, channel: str = None):
        global current
        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            if not ctx.voice_client.is_playing():
                def err(e):
                    print('Player error: %s' % e) if e else None
                    self.next_music(ctx)
                current[0] = player
                ctx.voice_client.play(player, after=err)
                await ctx.send('Tocando: {}'.format(player.title))
            else:
                players.append(player)
                await ctx.send('{} adicionada na fila'.format(player.title))
    
    @commands.command()
    async def skip(self, ctx: Context):
        ctx.voice_client.stop()
    
    @commands.command()
    async def stream(self, ctx: Context, url: str, channel: str = None):
        global current
        async with ctx.typing():
            player = await YTDLSource.from_url(url, stream=True)
            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                current[0] = player
                await ctx.send('Tocando: {}'.format(player.title))
            else:
                players.append(player)
                await ctx.send('{} adicionada na fila'.format(player.title))

    @commands.command()
    async def loop(self, ctx: Context):
        global loop
        loop = not loop
        await ctx.message.add_reaction('✅')
        if loop:
            await ctx.send('Música em Looping')
        else:
            await ctx.send('Não está mais em Looping')
        

    @commands.command()
    async def stop(self, ctx: Context, channel: str = None):
        players.clear()
        current.clear()
        ctx.voice_client.stop()
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def leave(self, ctx: Context, channel: str = None):
        if ctx.author.name != "SmileyDroid" :
            await ctx.author.send('Você não é o sorriso, você é {}'.format(ctx.author.name))
            return
        # voice_channel, connected, client = get_voice_channel_and_status(
        #    ctx, channel)

        if ctx.voice_client != None and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send("Não estou conectado")
    
    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
