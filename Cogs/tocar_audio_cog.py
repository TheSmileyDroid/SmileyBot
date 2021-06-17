import asyncio
from gtts.tts import gTTS
from utils import get_voice_channel_and_status, get_voice_client, voice_clients
import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context
import pafy


class TocarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: Context, url: str, channel: str = None):
        voice = await get_voice_client(ctx, channel)

        video = pafy.pafy.new(url)
        voice.play(discord.FFmpegPCMAudio(video.audiostreams[0].url))
        while voice.is_playing():
            await asyncio.sleep(1)
        voice.stop()

    @commands.command()
    async def stop(self, ctx: Context, channel: str = None):
        voice_channel, connected, client = get_voice_channel_and_status(
            ctx, channel)

        if connected:
            client.stop()
        else:
            await ctx.send("Eu num to tocando musica")

    @commands.command()
    async def leave(self, ctx: Context, channel: str = None):
        voice_channel, connected, client = get_voice_channel_and_status(
            ctx, channel)

        if connected:
            await client.disconnect()
            voice_clients.remove(client)
        else:
            await ctx.send("Eu num to conectado loco")
