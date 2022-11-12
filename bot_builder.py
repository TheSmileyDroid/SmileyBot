import asyncio
from typing import Type
import discord
from discord.ext import commands


class BotBuilder:
    def __init__(self) -> None:
        """
        Initialize the bot.
        """
        intents = discord.Intents.all()
        self.bot: commands.Bot = commands.Bot(
            command_prefix="-",
            strip_after_prefix=True,
            case_insensitive=True,
            intents=intents,
        )

    def add_cog(self: commands.Cog, cog: Type[commands.Cog]):
        """
        Adds a cog to the bot.

        Args:
            self: The bot.
            cog: The cog to add.
        """
        try:
            loop = asyncio.get_event_loop()
            coroutine = self.bot.add_cog(cog(self.bot))
            loop.run_until_complete(coroutine)
        except Exception as e:
            print(f"Error when adding cog: {e}")
            self.bot.add_cog(cog(self.bot))

    def remove_cog(self, cog_name: str):
        self.bot.remove_cog(cog_name)

    def run(self, idx: str):
        self.bot.run(idx)
