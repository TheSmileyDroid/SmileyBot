import os

import discord

from app import keep_alive
from bot_builder import BotBuilder
import asyncio

discord.opus.load_opus("./libopus.so.0.8.0")
bot = BotBuilder()

if __name__ == "__main__":
    # Add cogs
    for f in os.listdir("./Cogs"):
        if f.endswith(".py"):
            bot.bot.load_extension("Cogs." + f[:-3])

    # Connect
    bot.run(os.environ["DISCORD_ID"])