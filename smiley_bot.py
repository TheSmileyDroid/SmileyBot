import os
from bot_builder import BotBuilder
from Cogs import default_cog, tocar_audio_cog, reddit_cog, rodrigo_cog#, cassino_cog, falar_cog
from keep_alive import keep_alive

if __name__ == '__main__':
    bot = BotBuilder()
    # Add cogs
    bot.add_cog(default_cog.DefaultCog)
    # bot.add_cog(falar_cog.FalarCog)
    bot.add_cog(tocar_audio_cog.TocarCog)
    bot.add_cog(reddit_cog.RedditCog)
    bot.add_cog(rodrigo_cog.RodrigoCog)
    # bot.add_cog(cassino_cog.CassinoCog)

    # Mantenha o bot rodando
    keep_alive()
    # Connect
    # print(os.environ['DISCORD_ID'])
    bot.run(os.environ['DISCORD_ID'])
