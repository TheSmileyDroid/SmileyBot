import random
from typing import TypeVar

import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands.context import Context

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4
}

ffmpeg_options = {
    "options": "-vn",
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music:
    url: str = ""
    title: str = ""

    def __init__(self, url: str = "", title: str = ""):
        self.url = url
        self.title = title

    @classmethod
    def from_url(cls, url: str):
        """
        This function is used to get the music from the url.
        :param cls:
        :param url:
        :return:
        """
        result = []
        data = ytdl.extract_info(url, download=False)
        if isinstance(data, dict):
            if "entries" in data:
                for entry in data["entries"]:
                    music = Music()
                    music.url = entry["url"]
                    music.title = entry["title"]
                    result.append(music)
                return result
            else:
                music = Music()
                music.url = data["url"]
                music.title = data["title"]
                result.append(music)
                return result
        return result

    def __str__(self) -> str:
        return f"{self.title}"


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self,
                 source: discord.FFmpegPCMAudio,
                 *,
                 data: dict,
                 volume: float = 0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = self.data.get("title")
        self.url = self.data.get("url")

    @classmethod
    async def from_url(cls: type, url: str) -> list:
        """Returns a list of YTDLSource objects from a URL"""

        initial_data = ytdl.extract_info(url, download=False)
        if isinstance(initial_data, dict):
            sources = []
            if "entries" in initial_data:
                for entry in initial_data["entries"]:
                    filename = entry["url"]
                    sources.append(
                        cls(
                            discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                            data=entry,
                        ))
                return sources
            else:
                filename = initial_data["url"]
                sources.append(
                    cls(
                        discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                        data=initial_data,
                    ))
                return sources
        return []

    @classmethod
    async def from_music(cls: TypeVar("YTDLSource"), music: Music) -> list:
        """Returns a list of YTDLSource objects from a Music object"""

        data = ytdl.extract_info(music.url, download=False)
        data["title"] = music.title
        return cls(discord.FFmpegPCMAudio(data["url"], **ffmpeg_options),
                   data=data)


class Audio(commands.Cog):

    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.current_player: dict[str, Music] = {}  # {url: str, title: str}
        self.players: dict[str, list[Music]] = {}
        self.looping: dict[str, bool] = {}
        self.skips: dict[str, bool] = {}

    def check_voice(self, ctx: Context) -> bool:
        """
        Check if the bot is in a voice channel.

        :param self: The bot object.
        :param ctx: The context object.
        :return: True if the bot is in a voice channel, False otherwise.
        """
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        """Inicia o bot de audio"""
        print("[Audio] Iniciando...")
        for guild in self.bot.guilds:
            self.current_player[str(guild.id)] = Music()
            self.players[str(guild.id)] = []
            self.looping[str(guild.id)] = False
            self.skips[str(guild.id)] = False
            print(f"[Audio] Iniciado em {guild.name}[{guild.id}]")
        print("[Audio] Pronto!")

    async def play_next(self, ctx: Context, e=None):
        print(f"[ERROR] Player error: {e} ({ctx.guild}[{ctx.guild.id}])"
              ) if e else None
        if self.looping[str(
                ctx.guild.id)] and not self.skips[str(ctx.guild.id)]:
            print(f"[Audio] Repetindo {ctx.guild.name}[{ctx.guild.id}]")
            player = await YTDLSource.from_url(self.current_player[str(
                ctx.guild.id)].url)
            ctx.voice_client.play(
                player[0],
                after=lambda er: self.bot.loop.create_task(
                    (self.play_next(ctx, er))),
            )
        elif len(self.players[str(ctx.guild.id)]) > 0:
            if not ctx.voice_client.is_playing():
                player = self.players[str(ctx.guild.id)].pop(0)
                ctx.voice_client.play(
                    (await YTDLSource.from_music(player)),
                    after=lambda er: self.bot.loop.create_task(
                        (self.play_next(ctx, er))),
                )
                self.current_player[str(ctx.guild.id)] = player
                self.skips[str(ctx.guild.id)] = False
        else:
            self.current_player[str(ctx.guild.id)].url = ""
            self.current_player[str(ctx.guild.id)].title = ""
            self.skips[str(ctx.guild.id)] = False

    @commands.command()
    async def play(self, ctx: Context, url: str):
        """Toca uma música de uma URL"""
        await self.voice(ctx)
        musics: list[Music] = Music.from_url(url)
        music: YTDLSource = await YTDLSource.from_music(music=musics[0])

        if self.current_player[str(ctx.guild.id)].url == "":
            print(
                f"[INFO] Tocando {format(music.title)}({ctx.guild}[{ctx.guild.id}] in {ctx.author}[{ctx.author.id}])"
            )
            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(
                    music,
                    after=lambda e: self.bot.loop.create_task(
                        (self.play_next(ctx, e))),
                )
                self.current_player[str(ctx.guild.id)].url = music.url
                self.current_player[str(ctx.guild.id)].title = format(
                    music.title)
                await ctx.send(f"Tocando **{music.title}**!!!!")
        else:
            print(
                f"[INFO] ** {format(musics[0].title)} ** adicionado a fila({ctx.guild}[{ctx.guild.id}])"
            )
            self.players[str(ctx.guild.id)].append(music)
            await ctx.send(f"**{musics[0].title}** adicionado a fila")

        for m in musics[1:]:
            self.players[str(ctx.guild.id)].append(m)
            print(
                f"[INFO] ** {m.title} ** adicionado a fila({ctx.guild}[{ctx.guild.id}])"
            )
            await ctx.send(f"**{m.title}** adicionada a fila")

    @commands.command()
    async def stop(self, ctx: Context):
        """Para de tocar"""
        await self.voice(ctx)
        ctx.voice_client.stop()
        self.players[str(ctx.guild.id)] = []
        self.current_player[str(ctx.guild.id)].url = ""
        self.current_player[str(ctx.guild.id)].title = ""
        await ctx.send("Musica parada!")

    @commands.command()
    async def queue(self, ctx: Context):
        """Mostra a fila de músicas"""
        if self.current_player[str(ctx.guild.id)] != "":
            text = f"**SmileyBot [HARPI] :turtle:**\n\n"
            text += f'Loop: {"Músicas em looping" if self.looping[str(ctx.guild.id)] else "Não está em looping"}\n\n'
            text += f"** Musica atual: {self.current_player[str(ctx.guild.id)].title} **\n\n"
            if len(self.players[str(ctx.guild.id)]) > 0:
                text += "Fila:\n"
                for i, music in enumerate(self.players[str(ctx.guild.id)]):
                    text += f" {i}. __{music.title}__\n"
            await ctx.send(text)
        else:
            await ctx.send("Não há músicas na fila!")

    @commands.command()
    async def skip(self, ctx: Context):
        """Pula a música atual"""
        await self.voice(ctx)
        self.skips[str(ctx.guild.id)] = True
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            if self.current_player[str(ctx.guild.id)].url == "":
                await ctx.send("Não há nada tocando")
                return
            ctx.voice_client.stop()
        await ctx.send("Música pulada!")

    @commands.command()
    async def loop(self, ctx: Context):
        """Repete a música atual"""
        await self.voice(ctx)
        self.looping[str(ctx.guild.id)] = not self.looping[str(ctx.guild.id)]

        await ctx.send("Música sendo repetida!" if self.looping[str(
            ctx.guild.id)] else "Música não está mais sendo repetida!")

    @commands.command()
    async def pause(self, ctx: Context):
        """Pausa a música atual"""
        await self.voice(ctx)
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada!")
        else:
            await ctx.send("Não há nada tocando!")

    @commands.command()
    async def resume(self, ctx: Context):
        """Resume a música atual"""
        await self.voice(ctx)
        if ctx.voice_client is None:
            return await ctx.send("Não há nada tocando!")
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música resumida!")
        else:
            await ctx.send("Não há nada pausado!")

    @commands.command()
    async def shuffle(self, ctx: Context):
        """Embaralha a fila de músicas"""
        await self.voice(ctx)
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        random.shuffle(self.players[str(ctx.guild.id)])
        await ctx.send("Fila embaralhada!")

    @commands.command()
    async def remove(self, ctx: Context, index: int):
        """Remove uma música da fila"""
        await self.voice(ctx)
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        if index > len(self.players[str(ctx.guild.id)]) - 1:
            await ctx.send("Index inválido!")
            return
        self.players[str(ctx.guild.id)].pop(index)
        await ctx.send("Música removida!")

    @commands.command()
    async def clear(self, ctx: Context):
        """Limpa a fila de músicas"""
        await self.voice(ctx)
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        if self.players[str(ctx.guild.id)] == []:
            await ctx.send("A fila está vazia!")
        else:
            self.players[str(ctx.guild.id)] = []
            await ctx.send("Fila limpa!")

    @commands.command()
    async def leave(self, ctx: Context):
        """Desconecta o bot do canal de voz"""
        await self.voice(ctx)
        if isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.voice_client, discord.VoiceClient):
            await ctx.voice_client.disconnect()
            self.players[str(ctx.guild.id)] = []
            self.current_player[str(ctx.guild.id)].url = ""
            self.current_player[str(ctx.guild.id)].title = ""
            await ctx.send("Desconectado!")

    async def voice(self, ctx: Context):
        """Conecta o bot ao canal de voz"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Você não está conectado em um canal de voz")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif (ctx.author.voice
              and ctx.voice_client.channel != ctx.author.voice.channel):
            await ctx.send("Você não está conectado em um canal de voz ou\
                         o bot está em outro canal de voz")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
        if not self.check_voice(ctx):
            raise commands.CommandError(
                "Bot not connected to a voice channel.")


def setup(client):
    client.add_cog(Audio(client))
