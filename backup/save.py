from discord.file import File
import requests
import os
import io
import youtube_dl
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import asyncio
from typing import Union

from discord.voice_client import VoiceClient
from gtts import gTTS
import discord
import pafy
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.audiorec import NativeVoiceClient
import speech_recognition as sr

bot = commands.Bot(command_prefix="%")

voice_clients: list[discord.VoiceClient] = []

r = sr.Recognizer()




def is_connected(voice_channel: discord.VoiceChannel) -> Union[bool, discord.VoiceClient]:
    for client in voice_clients:
        if client.channel == voice_channel:
            return True, client
    return False, None


@bot.command()
async def test(ctx: Context, args: str):

    await ctx.send(args)


@bot.command()
async def chat(ctx: Context, args: str):
    print(ctx.author.display_name + ': ' + args)
    response = chatbot.get_response(args)
    print(response)
    await ctx.send("Loco: {}".format(response))


@bot.command()
async def play(ctx: Context, url: str, channel: str = None):
    voice = await get_voice_client(ctx, channel)

    video = pafy.pafy.new(url)
    voice.play(discord.FFmpegPCMAudio(video.audiostreams[0].url))
    while voice.is_playing():
        await asyncio.sleep(1)
    voice.stop()


@bot.command()
async def listen(ctx: Context, channel: str = None):
    voice = await get_voice_client(ctx, channel)

    voice.record(lambda e: print(f"Exception: {e}"))
    print("Started record")

    await asyncio.sleep(10)

    print("Finalizando a gravação")

    wav_bytes = await voice.stop_record()

    wav_file = discord.File(io.BytesIO(wav_bytes), filename="Recorded.wav")

    await ctx.send(file=wav_file)

    with open("Recorded.wav", "wb") as fh:
        fh.write(io.BytesIO(wav_bytes).read())

    with sr.AudioFile("Recorded.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="pt-BR")
        await ctx.send("Transcrição do audio: {}".format(text))
    # voice.play(discord.FFmpegPCMAudio(audio_binaries))


@bot.command()
async def responda(ctx: Context, channel: str = None):
    voice = await get_voice_client(ctx, channel)

    voice.record(lambda e: print(f"Exception: {e}"))
    print("Started record")

    await asyncio.sleep(10)

    print("Finalizando a gravação")

    wav_bytes = await voice.stop_record()

    wav_file = discord.File(io.BytesIO(wav_bytes), filename="Recorded.wav")

    await ctx.send(file=wav_file)

    with open("Recorded.wav", "wb") as fh:
        fh.write(io.BytesIO(wav_bytes).read())

    with sr.AudioFile("Recorded.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="pt-BR")
        await ctx.send("Transcrição do audio: {}".format(text))

    print(ctx.author.display_name + ': ' + text)
    response = str(chatbot.get_response(text))
    await ctx.send("Loco: {}".format(response))
    print(response)

    tts = gTTS(text=response, lang="pt-br", slow=False)

    tts.save("audio.mp3")

    voice.play(discord.FFmpegPCMAudio("audio.mp3"))

    while voice.is_playing():
        await asyncio.sleep(1)
    voice.stop()


@bot.command()
async def stop(ctx: Context, channel: str = None):
    voice_channel, connected, client = get_voice_channel_and_status(
        ctx, channel)

    if connected:
        client.stop()
    else:
        await ctx.send("Eu num to tocando musica")


@bot.command()
async def leave(ctx: Context, channel: str = None):
    voice_channel, connected, client = get_voice_channel_and_status(
        ctx, channel)

    if connected:
        await client.disconnect()
        voice_clients.remove(client)
    else:
        await ctx.send("Eu num to conectado loco")


@bot.command()
async def falar(ctx: Context, text: str, channel: str = None, lang: str = "pt-br"):
    voice = await get_voice_client(ctx, channel)

    tts = gTTS(text=text, lang=lang, slow=False)

    tts.save("audio.mp3")

    voice.play(discord.FFmpegPCMAudio("audio.mp3"))

    while voice.is_playing():
        await asyncio.sleep(1)
    voice.stop()
    
    #await falar_by_cmd(voice)


@bot.command()
async def falartts(ctx: Context, args: str, channel: str = None, lang: str = "pt-br"):
    voice = await get_voice_client(ctx, channel)

    print(ctx.author.display_name + ': ' + args)
    response = str(chatbot.get_response(args))
    print(response)

    tts = gTTS(text=response, lang=lang, slow=False)

    tts.save("audio.mp3")

    voice.play(discord.FFmpegPCMAudio("audio.mp3"))
    await ctx.send("Loco: {}".format(response))

    while voice.is_playing():
        await asyncio.sleep(1)
    voice.stop()


async def get_voice_client(ctx, channel):
    voice_channel, connected, voice = get_voice_channel_and_status(
        ctx, channel)
    if not connected:
        voice: VoiceClient = await voice_channel.connect()
        voice_clients.append(voice)
    return voice


def get_voice_channel_and_status(ctx, channel):
    if channel is not None:
        voice_channel = discord.utils.get(
            ctx.guild.voice_channels, name=channel)
    else:
        voice_channel = ctx.author.voice.channel
    connected, voice = is_connected(voice_channel)
    return voice_channel, connected, voice


@bot.event
async def on_ready():
    print("Conectado como {0}".format(bot.user.display_name))

async def falar_by_cmd(voice):
    while voice:
        tts = gTTS(text=input('Falar: '), lang='pt-BR', slow=False)

        tts.save("audio.mp3")

        voice.play(discord.FFmpegPCMAudio("audio.mp3"))

        while voice.is_playing():
            await asyncio.sleep(1)
        voice.stop()

if __name__ == '__main__':
    bot.run('ODM2MzU5NTUxNTQzODAzOTI1.YIc2hw.qHNx912yiY9DABa6MVb-FNZaPQI')
