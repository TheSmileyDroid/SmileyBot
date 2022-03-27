import os
from bot_builder import BotBuilder
from Cogs import (default_cog, tocar_audio_cog, reddit_cog, falar_cog)
from keep_alive import keep_alive

bot = BotBuilder()

if __name__ == '__main__':
    # Add cogs
    bot.add_cog(default_cog.Basic)
    bot.add_cog(falar_cog.Falar)
    bot.add_cog(tocar_audio_cog.Audio)
    bot.add_cog(reddit_cog.Reddit)

    # Keep the bot running
    keep_alive()

    # Connect
    bot.run(os.environ['DISCORD_ID'])
