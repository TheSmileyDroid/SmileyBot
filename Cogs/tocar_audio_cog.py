import discord
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
    'source_address': '0.0.0.0'  # bind to ipv4
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = self.data.get('title')
        self.url = self.data.get('url')

    @classmethod
    async def from_url(cls, url) -> list:
        '''Returns a list of YTDLSource objects from a URL'''

        initial_data = ytdl.extract_info(url, download=False)
        sources = []
        if 'entries' in initial_data:
            for entry in initial_data['entries']:
                filename = entry['url']
                sources.append(cls(discord.FFmpegPCMAudio(filename,
                               **ffmpeg_options), data=entry))
            return sources
        else:
            filename = initial_data['url']
            sources.append(cls(discord.FFmpegPCMAudio(
                filename, **ffmpeg_options), data=initial_data))
            return sources


class Audio(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.current_player: dict[str, YTDLSource] = {}
        self.players: dict[str, list[YTDLSource]] = {}
        self.loopings: dict[str, bool] = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        '''Inicia o bot de audio'''
        print('[Audio] Iniciando...')
        for guild in self.bot.guilds:
            self.current_player[str(guild.id)] = None
            self.players[str(guild.id)] = []
            self.loopings[str(guild.id)] = False
            print(f'[Audio] Iniciado em {guild.name}[{guild.id}]')
        print('[Audio] Pronto!')

    def play_next(self, ctx: Context, e=None):
        print(
            f'[ERROR] Player error: {e} ({ctx.guild}[{ctx.guild.id}])') if e else None
        if self.loopings[str(ctx.guild.id)] and self.current_player[str(ctx.guild.id)] is not None:
            print(f'[Audio] Repetindo {ctx.guild.name}[{ctx.guild.id}]')
            player = YTDLSource.from_url(self.current_player[str(ctx.guild.id)].url)
            ctx.voice_client.play(
                        player, after=lambda e: self.play_next(ctx, e))
            self.current_player[str(ctx.guild.id)] = player
        elif len(self.players[str(ctx.guild.id)]) >= 0:
            if not ctx.voice_client.is_playing():
                player = self.players[str(ctx.guild.id)].pop(0)
                ctx.voice_client.play(
                    player, after=lambda e: self.play_next(ctx, e))
                self.current_player[str(ctx.guild.id)] = player
        else:
            self.current_player[str(ctx.guild.id)] = None

    @commands.command()
    async def play(self, ctx: Context, url: str):
        '''Toca uma música de uma URL'''
        musics = await YTDLSource.from_url(url, ctx=ctx)
        music = musics[0]

        if self.current_player[str(ctx.guild.id)] is None:
            print(
                f'[INFO] Tocando {format(music.title)} ({ctx.guild}[{ctx.guild.id}])')
            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(
                    music, after=lambda e: self.play_next(ctx, e))
                self.current_player[str(ctx.guild.id)] = music
            if not ctx.voice_client.is_playing():
                await ctx.send(f'Tocando **{music.title}**!!!!')
        else:
            print(
                f'[INFO] **{format(musics[0].title)}** adicionado a fila ({ctx.guild}[{ctx.guild.id}])')
            self.players[str(ctx.guild.id)].append(music)
            await ctx.send(f'**{musics[0].title}** adicionado a fila')

        for i in range(1, len(musics)):
            self.players[str(ctx.guild.id)].append(musics[i])

    @commands.command()
    async def stop(self, ctx: Context):
        '''Para de tocar'''
        ctx.voice_client.stop()
        self.players[str(ctx.guild.id)] = []
        self.current_player[str(ctx.guild.id)] = None
        await ctx.send('Musica parada!')

    @commands.command()
    async def queue(self, ctx: Context):
        '''Mostra a fila de músicas'''
        if self.current_player[str(ctx.guild.id)] is not None:
            text = f'**Musica atual: {self.current_player[str(ctx.guild.id)].title}**\n\n'
            text += 'Fila:\n'
            for music in self.players[str(ctx.guild.id)]:
                if music.title is not None:
                    text += f'__{format(music.title)}__\n'
            await ctx.send(text)
        else:
            await ctx.send('Não há músicas na fila!')

    @commands.command()
    async def skip(self, ctx: Context):
        '''Pula a música atual'''
        if self.current_player[str(ctx.guild.id)] is None:
            await ctx.send('Não há nada tocando')
            return
        ctx.voice_client.stop()

        await ctx.send('Música pulada!')

    @commands.command()
    async def loop(self, ctx: Context):
        '''Repete a música atual'''
        
        self.loopings[str(ctx.guild.id)] = not self.loopings[str(ctx.guild.id)]

        await ctx.send(
            'Música sendo repetida!'
            if self.loopings[str(ctx.guild.id)]
            else 'Música não está mais sendo repetida!')

    @play.before_invoke
    @stop.before_invoke
    async def voice(self, ctx):
        '''Conecta o bot ao canal de voz'''
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(
                    "Você não está conectado em um canal de voz")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        else:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await ctx.send(
                        "Você não está conectado em um canal de voz ou\
                         o bot está em outro canal de voz")
                    raise commands.CommandError(
                        "Author not connected to a voice channel.")
