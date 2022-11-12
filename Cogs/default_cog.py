import asyncio
from discord import Member, VoiceChannel
from discord.ext import commands
from discord.ext.commands.context import Context


class Basic(commands.Cog):
    """Usado para testes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect_to_voice(self, ctx: Context) -> None:
        """Conecta o bot a um canal de voz"""
        if isinstance(ctx.author, Member):
            autor: Member = ctx.author
            if not isinstance(autor.voice, VoiceChannel):
                await ctx.send("Você precisa estar em um canal de voz")
                return
            if not isinstance(autor.voice.channel, VoiceChannel):
                await ctx.send("Você precisa estar em um canal de voz")
                return
            await autor.voice.channel.connect()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Connected as {self.bot.user.display_name}")

    @commands.command()
    async def test(self, ctx: Context, args: str):
        await ctx.send(args)

    @commands.command()
    async def move(self, _ctx: Context, user: Member, channel: VoiceChannel):
        await user.edit(voice_channel=channel)

    @commands.command()
    async def list_voice_channels(self, ctx: Context):
        await ctx.send()

def setup(client):
	client.add_cog(Basic(client))