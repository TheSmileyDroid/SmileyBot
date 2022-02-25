from discord import Member, VoiceChannel
from discord.ext import commands
from discord.ext.commands.context import Context


class Basic(commands.Cog):
    '''Usado para testes'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect_to_voice(self, ctx: Context):
        '''Conecta o bot a um canal de voz'''
        if isinstance(ctx.author, Member):
            autor: Member = ctx.author
            await autor.voice.channel.connect()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Connected as {self.bot.user.display_name}')

    @commands.command()
    async def test(self, ctx: Context, args: str):
        await ctx.send(args)

    @commands.command()
    async def move(self, _ctx: Context, user: Member, channel: VoiceChannel):
        await user.edit(voice_channel=channel)

    @commands.command()
    async def list_voice_channels(self, ctx: Context):
        await ctx.send()