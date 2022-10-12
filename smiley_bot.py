import os

from bot_builder import BotBuilder
from Cogs import (default_cog, tocar_audio_cog, reddit_cog, falar_cog, rpg_cog)
from app import keep_alive
import discord

discord.opus.load_opus('./libopus.so.0.8.0')

bot = BotBuilder()

if __name__ == '__main__':
    # Add cogs
    bot.add_cog(default_cog.Basic)
    bot.add_cog(falar_cog.Falar)
    bot.add_cog(tocar_audio_cog.Audio)
    bot.add_cog(rpg_cog.RPG)

    # Keep 
    keep_alive()

    # Connect
    bot.run(os.environ['DISCORD_ID'])
