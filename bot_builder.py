from typing import Type
import discord
from discord.ext import commands


class BotBuilder():

    def __init__(self):
        self.bot: commands.Bot = commands.Bot(command_prefix="-",
                                              strip_after_prefix=True,
                                              case_insensitive=True)

    def add_cog(self, cog: Type[commands.Cog]):
        self.bot.add_cog(cog(self.bot))

    def remove_cog(self, cog_name: str):
        self.bot.remove_cog(cog_name)

    def run(self, idx: str):
        self.bot.run(idx)
        
