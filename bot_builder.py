from typing import Type
import discord
from discord.ext import commands
import asyncio

class BotBuilder():

    def __init__(self):
      intents = discord.Intents.all()
      self.bot: commands.Bot = commands.Bot(command_prefix="-",
                                              strip_after_prefix=True,
                                              case_insensitive=True, intents=intents)

    def add_cog(self, cog: Type[commands.Cog]):
      try: 
        loop = asyncio.get_event_loop()
        coroutine = self.bot.add_cog(cog(self.bot))
        loop.run_until_complete(coroutine)
      except:
        self.bot.add_cog(cog(self.bot))

    def remove_cog(self, cog_name: str):
      self.bot.remove_cog(cog_name)

    def run(self, idx: str):
      self.bot.run(idx)
        
