import discord
from discord import *
from discord.ext import commands
from discord.ext.commands.context import Context


class DefaultCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected as {}'.format(self.bot.user.display_name))

    @commands.command()
    async def test(self, ctx: Context, args: str):
        await ctx.send(args)

    @commands.command()
    async def move(self, ctx: Context, user: Member, channel: VoiceChannel):
        await user.edit(voice_channel=channel)

    @commands.command()
    async def list_voice_channels(self, ctx: Context):
        await ctx.send()

    @commands.command()
    async def mute(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(mute=True)
        else:
            await ctx.send('Você não é o sorriso, você é {}'.format(ctx.author.name))

    @commands.command()
    async def unmute(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(mute=False)
        else:
            await ctx.send('Você não é o sorriso, você é {}'.format(ctx.author.name))

    @commands.command()
    async def deaf(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(deafen=True)
        else:
            await ctx.send('Você não é o sorriso, você é {}'.format(ctx.author.name))

    @commands.command()
    async def undeaf(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(deafen=False)
        else:
            await ctx.send('Você não é o sorriso, você é {}'.format(ctx.author.name))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        pass
