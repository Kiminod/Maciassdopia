
import os
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
MACIASDOPIA
Created by Kiminod_96 and Kermitello
Start by typing `help` \n ''')

settings = ["None", "None", "None", "None", "None"]
payload = ""

def createTable(settings):
    table = PrettyTable(["Setting", "Value"])
    table.add_row(["Backdoor Name", settings[0]])

    if payload == "discord":
        table.add_row(["Guild ID", settings[1]])
        table.add_row(["Bot Token", settings[2]])
        table.add_row(["Channel ID", settings[3]])
        table.add_row(["Keylogger Webhook", settings[4]])
    else:
        print("[!] Please select a payload!\n")
    return table

try:
    while True:
        command = input(f"[+] {payload} > ")
        command_list = command.split()

        if command_list == []:
            continue
            
        if command_list[0] == "exit":
            print("\n[+] Exiting!")
            exit()

        elif command_list[0] == "use":
            if len(command_list) == 1:
                print("[!] Please specify a payload!")
            else:
                if command_list[1] == "discord":
                    print("[+] Using Discord")
                    payload = "discord"
                    table = createTable(settings)
                    print(f"\n{table.get_string(title='Maciassdopia Backdoor Settings')}")
                    print("Run 'help set' for more information\n")
                else:
                    print("[!] Invalid payload!")

        elif command_list[0] == "set":
            if len(command_list) < 3:
                print("[!] Please specify a settin!\n")
            else:
                if command_list[1] == "name":
                    settings[0] = command_list[2]
                
                elif command_list[1] == "guild-id":
                    settings[1] = command_list[2]

                elif command_list[1] == "bot-token":
                    settings[2] = command_list[2]

                elif command_list[1] == "channel-id":
                    settings[3] = command_list[2]

                else:
                    print("[!] Invalid setting!")

        elif command_list[0] == "config":
            if payload == "":
                print("[!] Please select a payload!")
            else:
                table = createTable(settings)
                print(f"\n{table.get_string(title='Maciassdopia Backdoor Settings')}")
                print("Run 'help set' for more information\n")

        elif command_list[0] == "clear" or command_list[0] == "cls":
            clear_screeen()
        
        else:
            print("[!] Invalid command!")

except KeyboardInterrupt:
    print("\n\n[+] Exiting")
