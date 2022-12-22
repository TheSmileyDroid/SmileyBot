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
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

    def add_cog(self: 'BotBuilder', cog: Type[commands.Cog]):
        """
        Adds a cog to the bot.

        Args:
            self: The bot.
            cog: The cog to add.
        """
        self.loop.run_until_complete(self.bot.add_cog(cog(self.bot)))

    def remove_cog(self, cog_name: str):
        self.bot.remove_cog(cog_name)  # type: ignore

    def run(self, idx: str):
        self.bot.run(idx)
