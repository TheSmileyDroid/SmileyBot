from discord import Member, VoiceChannel, VoiceState
from discord.ext import commands
from discord.ext.commands.context import Context


class Basic(commands.Cog):
    '''Usado para testes'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def connect_to_voice(self, ctx: Context):
        await ctx.author.voice.channel.connect()

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
            await ctx.send('Você não é o sorriso, você é {}'
                           .format(ctx.author.name))

    @commands.command()
    async def unmute(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(mute=False)
        else:
            await ctx.send('Você não é o sorriso, você é {}'
                           .format(ctx.author.name))

    @commands.command()
    async def deaf(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(deafen=True)
        else:
            await ctx.send('Você não é o sorriso, você é {}'
                           .format(ctx.author.name))

    @commands.command()
    async def undeaf(self, ctx: Context, user: Member):
        if ctx.author.name == "SmileyDroid":
            await user.edit(deafen=False)
        else:
            await ctx.send('Você não é o sorriso, você é {}'
                           .format(ctx.author.name))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member,
                                    before: VoiceState, after: VoiceState):
        if member.name == 'SmileyDroidLoco':
            if after.mute:
                await member.edit(mute=False)

    @commands.command()
    async def print_guild_info(self, ctx: Context):
        print("{}, canais: {}, canais de voz: {}"
              .format(ctx.guild, ctx.guild.channels, ctx.guild.voice_channels))
