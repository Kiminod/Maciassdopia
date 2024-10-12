
import discord
from code.discord.bot import BOT

class miningInteractButtons(discord.ui.View):
    def __init__(self, inv:str, id:str, bot:BOT):
        super().__init__()
        self.inv = inv
        self.id = id
        self.bot = bot

    @discord.ui.button(label = "Strat", style = discord.ButtonStyle.blurple, emoji = "🟩")
    async def startButton(self, interaction:discord.Interaction, button:discord.ui.Button):
        self.bot.active_mining = True

        my_embed = discord.Embed(
            title = f"Started mining on Agent#{self.id}",
            color = 0x00FF00
        )
        
        await interaction.response.send_message(
            embed = my_embed,
            ephemeral=True
        )

    @discord.ui.button(label = "Stop", style = discord.ButtonStyle.blurple, emoji = "🟥")
    async def stopButton(self, interaction:discord.Interaction, button:discord.ui.Button):
        self.bot.active_mining = False

        my_embed = discord.Embed(
            title = f"Stopped mining on Agent#{self.id}",
            color = 0x00FF00
        )
        
        await interaction.response.send_message(
            embed = my_embed,
            ephemeral=True
        )