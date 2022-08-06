import random
import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands.context import Context

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

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = self.data.get('title')
        self.url = self.data.get('url')

    @classmethod
    async def from_url(cls, url: str) -> list:
        '''Returns a list of YTDLSource objects from a URL'''

        initial_data = ytdl.extract_info(url, download=False)
        if isinstance(initial_data, dict):
            sources = []
            if 'entries' in initial_data:
                for entry in initial_data['entries']:
                    filename = entry['url']
                    sources.append(
                        cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                            data=entry))
                return sources
            else:
                filename = initial_data['url']
                sources.append(
                    cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                        data=initial_data))
                return sources
        return []


class Music():
    url: str = ''
    title: str = ''

    def __str__(self) -> str:
        return f'{self.title}'


class Audio(commands.Cog):

    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.current_player: dict[str, Music] = {}  # {url: str, title: str}
        self.players: dict[str, list[Music]] = {}
        self.loopings: dict[str, bool] = {}
        self.skip: dict[str, bool] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        '''Inicia o bot de audio'''
        print('[Audio] Iniciando...')
        for guild in self.bot.guilds:
            self.current_player[str(guild.id)] = Music()
            self.players[str(guild.id)] = []
            self.loopings[str(guild.id)] = False
            self.skip[str(guild.id)] = False
            print(f'[Audio] Iniciado em {guild.name}[{guild.id}]')
        print('[Audio] Pronto!')

    async def play_next(self, ctx: Context, e=None):
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            print(f'[ERROR] Player error: {e} ({ctx.guild}[{ctx.guild.id}])'
                  ) if e else None
            if self.loopings[str(ctx.guild.id)] and not self.skip[str(ctx.guild.id)]:
                print(f'[Audio] Repetindo {ctx.guild.name}[{ctx.guild.id}]')
                player = await YTDLSource.from_url(self.current_player[str(
                    ctx.guild.id)].url)
                ctx.voice_client.play(
                    player[0],
                    after=lambda e: self.bot.loop.create_task(
                        (self.play_next(ctx, e))))
            elif len(self.players[str(ctx.guild.id)]) > 0:
                if not ctx.voice_client.is_playing():
                    player = self.players[str(ctx.guild.id)].pop(0)
                    ctx.voice_client.play(
                        (await YTDLSource.from_url(player.url))[0],
                        after=lambda e: self.bot.loop.create_task(
                            (self.play_next(ctx, e))))
                    self.current_player[str(ctx.guild.id)] = player
                    self.skips[str(ctx.guild.id)] = False
            else:
                self.current_player[str(ctx.guild.id)].url = ''
                self.current_player[str(ctx.guild.id)].title = ''
                self.skips[str(ctx.guild.id)] = False

    @commands.command()
    async def play(self, ctx: Context, url: str):
        '''Toca uma música de uma URL'''
        musics: list[YTDLSource] = await YTDLSource.from_url(url)
        music: YTDLSource = musics[0]

        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            if self.current_player[str(ctx.guild.id)].url == '':
                print(
                    f'[INFO] Tocando {format(music.title)} ({ctx.guild}[{ctx.guild.id}])'
                )
                if not ctx.voice_client.is_playing():
                    ctx.voice_client.play(
                        music,
                        after=lambda e: self.bot.loop.create_task(
                            (self.play_next(ctx, e))))
                    self.current_player[str(ctx.guild.id)].url = music.url
                    self.current_player[str(ctx.guild.id)].title = format(
                        music.title)
                    await ctx.send(f'Tocando **{music.title}**!!!!')
            else:
                print(
                    f'[INFO] **{format(musics[0].title)}** adicionado a fila ({ctx.guild}[{ctx.guild.id}])'
                )
                music_data = Music()
                music_data.title = music.title
                music_data.url = music.url
                self.players[str(ctx.guild.id)].append(music_data)
                await ctx.send(f'**{musics[0].title}** adicionado a fila')

            for i in range(1, len(musics)):
                music_data: Music = Music()
                music_data.url = musics[i].url
                music_data.title = musics[i].title
                self.players[str(ctx.guild.id)].append(music_data)
                print(
                    f'[INFO] **{music_data.title}** adicionado a fila ({ctx.guild}[{ctx.guild.id}])'
                )
                await ctx.send(f'**{music_data.title}** adicionada a fila')

    @commands.command()
    async def stop(self, ctx: Context):
        '''Para de tocar'''
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            ctx.voice_client.stop()
            self.players[str(ctx.guild.id)] = []
            self.current_player[str(ctx.guild.id)].url = ''
            self.current_player[str(ctx.guild.id)].title = ''
            await ctx.send('Musica parada!')

    @commands.command()
    async def queue(self, ctx: Context):
        '''Mostra a fila de músicas'''
        if isinstance(ctx.guild, discord.Guild):
            if self.current_player[str(ctx.guild.id)] != '':
                text = f'**Musica atual: {self.current_player[str(ctx.guild.id)].title}**\n\n'
                text += 'Fila:\n'
                for i, music in enumerate(self.players[str(ctx.guild.id)]):
                    text += f' {i}. __{music}__\n'
                await ctx.send(text)
            else:
                await ctx.send('Não há músicas na fila!')

    @commands.command()
    async def skip(self, ctx: Context):
        '''Pula a música atual'''
        self.skip[str(ctx.guild.id)] = True
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            if self.current_player[str(ctx.guild.id)].url == '':
                await ctx.send('Não há nada tocando')
                return
            ctx.voice_client.stop()
        await ctx.send('Música pulada!')

    @commands.command()
    async def loop(self, ctx: Context):
        '''Repete a música atual'''
        if isinstance(ctx.guild, discord.Guild):
            self.loopings[str(
                ctx.guild.id)] = not self.loopings[str(ctx.guild.id)]

            await ctx.send('Música sendo repetida!' if self.loopings[str(
                ctx.guild.id)] else 'Música não está mais sendo repetida!')

    @commands.command()
    async def pause(self, ctx: Context):
        '''Pausa a música atual'''
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send('Música pausada!')
            else:
                await ctx.send('Não há nada tocando!')

    @commands.command()
    async def resume(self, ctx: Context):
        '''Resume a música atual'''
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.send('Música resumida!')
            else:
                await ctx.send('Não há nada pausado!')

    @commands.command()
    async def suffle(self, ctx: Context):
        '''Embaralha a fila de músicas'''
        if isinstance(ctx.guild, discord.Guild):
            random.shuffle(self.players[str(ctx.guild.id)])
            await ctx.send('Fila embaralhada!')

    @commands.command()
    async def remove(self, ctx: Context, index: int):
        '''Remove uma música da fila'''
        if isinstance(ctx.guild, discord.Guild):
            if index > len(self.players[str(ctx.guild.id)]) - 1:
                await ctx.send('Index inválido!')
                return
            self.players[str(ctx.guild.id)].pop(index)
            await ctx.send('Música removida!')

    @commands.command()
    async def clear(self, ctx: Context):
        '''Limpa a fila de músicas'''
        if isinstance(ctx.guild, discord.Guild):
            self.players[str(ctx.guild.id)] = []
            await ctx.send('Fila limpa!')

    @play.before_invoke
    @stop.before_invoke
    async def voice(self, ctx):
        '''Conecta o bot ao canal de voz'''
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Você não está conectado em um canal de voz")
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
