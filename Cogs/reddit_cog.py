import random
import discord
from discord import *
from discord.ext import tasks, commands
from discord.ext.commands.context import Context
import asyncpraw as praw
from asyncpraw import reddit

subreddits = ['cats', ]  # 'aww', ]  # , 'CuteAnimals']

cats = []


class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit: praw.Reddit = praw.Reddit(client_id='515a_Gyt37LPJA',
                                               client_secret='xS9hlckXGF_w0WqaM6SV5muhMFQmXg', user_agent='SmileyDroidLoco')
        self.update_cat.start()

    @commands.command()
    async def reddit_hot(self, ctx: Context, subreddit: str, number: int = 10):
        sub: reddit.Subreddit = await self.reddit.subreddit(subreddit)
        i = 0
        async for post in sub.hot(limit=100):
            if not post.is_self and i < number:  # We only want to work with link posts
                if post.url.endswith("jpg") or post.url.endswith("jpeg") or post.url.endswith("png"):
                    slink = post.url
                    await ctx.send(embed=discord.Embed(description=subreddit).set_image(url=slink))
                    i += 1

    @tasks.loop(minutes=20)
    async def update_cat(self):
        cats.clear()
        for subreddit in subreddits:
            sub: reddit.Subreddit = await self.reddit.subreddit(subreddit)

            async for post in sub.hot(limit=170):
                if not post.is_self:  # We only want to work with link posts
                    if post.url.endswith("jpg") or post.url.endswith("jpeg") or post.url.endswith("png"):
                        cats.append(post)
        print('Gatos atualizados')

    @commands.command()
    async def cat(self, ctx: Context):
        post = random.choice(cats)
        await ctx.send(embed=discord.Embed(description=post.subreddit).set_image(url=post.url))
