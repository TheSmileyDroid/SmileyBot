import gtts
import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class Falar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def f(self, ctx: Context, *, text: str):
        
        tts = gtts.tts.gTTS(text=text, lang="pt-br", slow=False)

        tts.save("cache/audio.mp3")
        if isinstance(ctx.voice_client, discord.VoiceClient):
            ctx.voice_client.play(discord.FFmpegPCMAudio("cache/audio.mp3"))

    @commands.command()
    async def n(self, ctx: Context, lang: str = "pt-br"):
        tts = gtts.tts.gTTS(text="não", lang=lang, slow=False)

        tts.save("cache/audio.mp3")
        if isinstance(ctx.voice_client, discord.VoiceClient):
            ctx.voice_client.play(discord.FFmpegPCMAudio("cache/audio.mp3"))

    @commands.command()
    async def s(self, ctx: Context, lang: str = "pt-br"):
        tts = gtts.tts.gTTS(text="sim", lang=lang, slow=False)

        tts.save("cache/audio.mp3")
        if isinstance(ctx.voice_client, discord.VoiceClient):
            ctx.voice_client.play(discord.FFmpegPCMAudio("cache/audio.mp3"))

    @f.before_invoke
    @s.before_invoke
    @n.before_invoke
    async def voice(self, ctx):
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
