import asyncio
import os
from typing import List

import discord

from app import keep_alive
from bot_builder import BotBuilder
from Cogs import (default_cog, falar_cog, math_cog, reddit_cog, rpg_cog,
                  script_cog, tocar_audio_cog)

# Load opus
discord.opus.load_opus("./libopus.so.0.8.0")
bot: BotBuilder = BotBuilder()

if __name__ == "__main__":
    # Add cogs
    bot.add_cog(default_cog.Basic)
    bot.add_cog(falar_cog.Falar)
    bot.add_cog(math_cog.Math)
    # bot.add_cog(reddit_cog.Reddit)
    bot.add_cog(rpg_cog.RPG)
    bot.add_cog(script_cog.Script)
    bot.add_cog(tocar_audio_cog.Audio)

    # Connect
    bot.run(os.environ["DISCORD_ID"])