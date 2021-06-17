from bot_builder import BotBuilder
from Cogs import default_cog, falar_cog, tocar_audio_cog, reddit_cog

if __name__ == '__main__':
    bot = BotBuilder()
    # Add cogs
    bot.add_cog(default_cog.DefaultCog)
    bot.add_cog(falar_cog.FalarCog)
    bot.add_cog(tocar_audio_cog.TocarCog)
    bot.add_cog(reddit_cog.RedditCog)

    # Connect
    bot.run('ODM2MzU5NTUxNTQzODAzOTI1.YIc2hw.qHNx912yiY9DABa6MVb-FNZaPQI')
