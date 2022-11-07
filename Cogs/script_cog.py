import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.context import Context


class Script(commands.Cog):
    def __init__(self, bot: commands.Bot):
        print()
        self.bot = bot
        self.scripts = {} # {user_id: {script_name: [script_code]}}
        self.editing = {} # {user_id: script_name}
        self.running = {} # {user_id: script_name}
        self.bot_msg = {} # {user_id: msg}

    @commands.Cog.listener()
    async def on_ready(self):
        print("[Script] Iniciando...")
        for guild in self.bot.guilds:
            for member in guild.members:
                self.scripts[member.id] = {}
                self.running[member.id] = False
            print(f"[Script] Iniciado em {guild.name}")
        print("[Script] Iniciado!")

    @commands.command(name='script', help='Executa uma série de comandos')
    async def script(self, ctx: Context, *, script: str):
        args = script.split()
        """
        **Executa uma série de comandos**
        
        Exemplo:
        ```
        -script new exemplo
        join
        play https://www.youtube.com/watch?v=XfTWgMgknpY
        wait 10
        pause
        say 734174031388868680 Bom dia!
        wait 10
        resume
        wait 10
        stop
        end

        -run exemplo
        ```
        """
        if script == 'help':
            await ctx.send("\
**Executa uma série de comandos**\n\
\n\
Exemplo:\n\
```\n\
-script new exemplo\n\
join\n\
play https://www.youtube.com/watch?v=XfTWgMgknpY\n\
wait 10\n\
pause\n\
say 734174031388868680 Bom dia!\n\
wait 10\n\
resume\n\
wait 10\n\
stop\n\
end\n\
\n\
-run exemplo\n\
```\n\
                ")
            return

        if script == 'list':
            await ctx.send(f'**Scripts:** {", ".join(self.scripts[ctx.author.id].keys())}')
            return
        
        if script == 'clear':
            self.scripts[ctx.author.id] = {}
            await ctx.send('**Scripts:** Todos os scripts foram apagados.')
            return
        
        if args[0] == 'new':
            script_name = script[4:]
            self.scripts[ctx.author.id][script_name] = []
            self.editing[ctx.author.id] = script_name
            await ctx.send(f'**Scripts:** Script {script_name} sendo editado. Use end para finalizar.')
            # Espera o usuário enviar o código do script
            return
        
        if script.startswith('import '):
            script_name = script[7: script.find('\n', 7)]
            script_code = script[script.find("```") + 3: script.rfind("```")]
            self.scripts[ctx.author.id][script_name] = script_code.split('\n')
            # Remove todos os comando vazios ('') do script
            self.scripts[ctx.author.id][script_name] = list(filter(None, self.scripts[ctx.author.id][script_name]))
            await ctx.send(f'**Scripts:** Script {script_name} importado como {self.scripts[ctx.author.id][script_name]}.')
            return


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id in self.editing:
            if message.content.startswith('-'):
                return
            if message.content == 'end':
                await message.channel.send(f'**Scripts:** Script {self.editing[message.author.id]} finalizado.')
                self.editing.pop(message.author.id)
                return
            if message.content == 'back':
                self.scripts = self.scripts[:-1]
                return
            script_name = self.editing[message.author.id]
            self.scripts[message.author.id][script_name].append(message.content)
            await message.delete()
            result = '\n'.join(self.scripts[message.author.id][script_name])
            if message.author.id in self.bot_msg:
                await self.bot_msg[message.author.id].edit(content=result+'\n\n_Esperando..._')
            else:
                self.bot_msg[message.author.id] = await message.channel.send(result+'\n\n_Esperando..._')
            return

    @commands.command(name='run', help='Executa um script')
    async def run(self, ctx: Context, script_name: str):

        if script_name == 'list':
            await ctx.send(f'**Scripts:** {", ".join(self.scripts[ctx.author.id].keys())}')
            return

        if script_name in self.scripts[ctx.author.id]:
            script = self.scripts[ctx.author.id][script_name]
            await ctx.send(f'**Scripts:** Executando script {script_name}')
            try:
                for line in script.copy():
                    if line.startswith('say '):
                        channel_id, text = line[4:].split(' ', 1)
                        channel = self.bot.get_channel(int(channel_id))
                        await channel.send(text)
                    elif line.startswith('wait '):
                        await asyncio.sleep(int(line[5:]))
                    else:
                        print(f'**Scripts:** Executando comando {line.split(" ")[0]}')
                        await ctx.invoke(self.bot.get_command(line.split(' ')[0]), *line.split(' ')[1:])
            except Exception as e:
                await ctx.send(f'**Scripts:** Erro ao executar script {script_name}: {e}')
                return
        else:
            await ctx.send(f'**Scripts:** Script {script_name} não encontrado.')


            