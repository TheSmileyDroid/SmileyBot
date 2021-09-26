import asyncio
import gtts
from utils import get_voice_client
import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context


class FalarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def f(self, ctx: Context, *text: str):
        #if ctx.author.name != "SmileyDroid" :
        #      await ctx.author.send('Você não é o sorriso, você é {}'.format(ctx.author.name))
        #      return
        #voice = await get_voice_client(ctx, None)
        txt = ''
        for t in text:
          txt += t + ' '
        tts = gtts.tts.gTTS(text=txt, lang="pt-br", slow=False)

        tts.save("cache/audio.mp3")

        ctx.voice_client.play(discord.FFmpegPCMAudio("cache/audio.mp3"))

    
    @commands.command()
    async def falar(self, ctx: Context, text: str, channel: str = None, lang: str = "pt-br"):
        #if ctx.author.name != "SmileyDroid" :
        #    await ctx.author.send('Você não é o sorriso, você é {}'.format(ctx.author.name))
        #    return
        voice = await get_voice_client(ctx, channel)

        tts = gtts.tts.gTTS(text=text, lang=lang, slow=False)

        tts.save("cache/audio.mp3")

        voice.play(discord.FFmpegPCMAudio("cache/audio.mp3"))

      
    @commands.command()
    async def n(self, ctx: Context, channel: str = None, lang: str = "pt-br"):
        #voice = await get_voice_client(ctx, channel)

        tts = gtts.tts.gTTS(text="não", lang=lang, slow=False)

        tts.save("audio.mp3")

        ctx.voice_client.play(discord.FFmpegPCMAudio("audio.mp3"))

    @commands.command()
    async def s(self, ctx: Context, channel: str = None, lang: str = "pt-br"):
        #voice = await get_voice_client(ctx, channel)

        tts = gtts.tts.gTTS(text="sim", lang=lang, slow=False)

        tts.save("audio.mp3")

        ctx.voice_client.play(discord.FFmpegPCMAudio("audio.mp3"))

    
    @f.before_invoke
    @falar.before_invoke
    @s.before_invoke
    @n.before_invoke
    async def voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Você não está conectado em um canal de voz")
                raise commands.CommandError("Author not connected to a voice channel.")
        else:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await ctx.send("Você não está conectado em um canal de voz ou o bot está em outro canal de voz")
                    raise commands.CommandError("Author not connected to a voice channel.")
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()