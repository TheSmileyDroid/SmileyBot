from typing import Type
import discord
from discord.ext import commands


class BotBuilder():
    def __init__(self):
        self.bot: discord.Client = commands.Bot(command_prefix="%")

    def add_cog(self, cog: Type[commands.Cog]):
        self.bot.add_cog(cog(self.bot))

    def remove_cog(self, cog_name: str):
        self.bot.remove_cog(cog_name)

    def run(self, id: str):
        self.bot.run(id)
