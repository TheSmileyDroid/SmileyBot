from typing import Union
from discord.voice_client import VoiceClient
import discord

voice_clients: list = []


def is_connected(voice_channel: discord.VoiceChannel) -> Union[bool, discord.VoiceClient]:
    for client in voice_clients:
        if client.channel == voice_channel:
            return True, client
    return False, None


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
