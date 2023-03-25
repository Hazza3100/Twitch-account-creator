import os
import re
import time
import random
import string
import requests
import threading

from os.path            import isfile, join
from colorama           import Fore



def checkFormat():
    pattern = r'^(?:(?P<user>[^:@]+):(?P<pass>[^:@]+)@)?(?P<host>[^:]+):(?P<port>\d+)$'
    proxies = open('data/proxies.txt', 'r').read().splitlines()
    for proxy in proxies:
        match = re.match(pattern, proxy)
        if match:
            return True
        else:
            return False

class captchaio:
    def __init__(self, apikey: str) -> None:
        self.session = requests.Session()
        self.apikey  = apikey
        self.headers = {'Host': 'api.capsolver.com', 'Content-Type': 'application/json'}

    def createTask(self, proxy: str) -> str:
        try:
            username, _, host      = proxy.partition(':')
            password, _, host_port = host.partition('@')
            hostname, _, port      = host_port.partition(':')
            json = {
                "clientKey": self.apikey,
                "task": {
                    "cd"           : True,
                    "pageURL"      : "https://passport.twitch.tv/integrity",
                    "proxyType"    : "http",
                    "proxyAddress" : hostname,
                    "proxyPort"    : int(port),
                    "proxyLogin"   : username,
                    "proxyPassword": password,
                    "userAgent"    : "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020",
                }
            }
            while True:
                r = self.session.post('https://api.capsolver.com/kasada/invoke', json=json, headers=self.headers)
                if "Proxy Ban" in r.text:
                    return False
                if r.json()['success'] == True:
                    x_kpsdk_ct = r.json()['solution']['x-kpsdk-ct']
                    x_kpsdk_cd = r.json()['solution']['x-kpsdk-cd']
                    return (x_kpsdk_cd, x_kpsdk_ct)
                else:
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Kasada Solve Error")
                    return False
        except:
            pass

def get_token(proxy: str, apikey) -> str:
    try:
        with requests.Session() as session:
            kas = captchaio(apikey).createTask(proxy)
            if kas == False:
                print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Kasada Solve Error")
            else:
                cd  = kas[0]
                ct  = kas[1]
                headers = {
                    "accept"           : "application/vnd.twitchtv.v3+json",
                    "accept-encoding"  : "gzip",
                    "accept-language"  : "en-us",
                    "api-consumer-type": "mobile; Android/1403020",
                    "client-id"        : "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                    "connection"       : "Keep-Alive",
                    "content-length"   : "0",
                    "host"             : "passport.twitch.tv",
                    "user-agent"       : "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020",
                    "x-app-version"    : "14.3.2",
                    "x-kpsdk-cd"       : cd,
                    "x-kpsdk-ct"       : ct,
                    "x-kpsdk-v"        : "a-1.6.0"
                    }
                r = session.post('https://passport.twitch.tv/integrity', headers=headers, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
                if "token" in r.text:
                    return r.json()['token']
                else:
                    return False
    except:
        pass



created = 0


def get_username():
    try:
        with requests.Session() as session:
            username = session.get('https://names.drycodes.com/10').json()[0]
            headers = {'Accept': '*/*','Accept-Language': 'en-GB','Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko','Connection': 'keep-alive','Content-Type': 'text/plain;charset=UTF-8','Origin': 'https://www.twitch.tv','Referer': 'https://www.twitch.tv/','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36','sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"',}
            data = '[{"operationName":"UsernameValidator_User","variables":{"username":"'+username+'"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660"}}}]'
            r = session.post('https://gql.twitch.tv/gql', data=data, headers=headers).json()[0]["data"]["isUsernameAvailable"]
            if r == True:
                return username
            else:
                return username + ''.join(random.choices('poiuytrewqlkjhgfdsaamnbvcxz', k=3))
    except:
        pass


def Gen(apikey: str):
    try:
        with requests.Session() as session:
            global created
            email    = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz0987654321', k=10)) + "@gmail.com"
            username = get_username()
            password = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz0987654321', k=12))
            proxy = random.choice(open('data/proxies.txt', 'r').read().splitlines())
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            integrity = get_token(proxy, apikey)
            if integrity is None or integrity == False:
                print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Failed to Fetch Integrity")
                pass
            else:
                headers = {
                    "accept"           : "application/vnd.twitchtv.v3+json",
                    "accept-encoding"  : "gzip",
                    "accept-language"  : "en-us",
                    "api-consumer-type": "mobile; Android/1403020",
                    "client-id"        : "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                    "connection"       : "Keep-Alive",
                    "content-length"   : "251",
                    "content-type"     : "application/json; charset=UTF-8",
                    "host"             : "passport.twitch.tv",
                    "user-agent"       : "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020",
                    "x-app-version"    : "14.3.2",
                    "x-device-id"      : ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                }
                json = {
                    "birthday": {
                        "day"  : random.randint(1,28),
                        "month": random.randint(1,12),
                        "year" : random.randint(1970,2005)
                    },
                    "client_id"                : "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                    "email"                    : email,
                    "include_verification_code": True,
                    "integrity_token"          : integrity,
                    "password"                 : password,
                    "username"                 : username
                }
                r = session.post('https://passport.twitch.tv/protected_register', json=json, headers=headers, proxies=proxies)
                if r.json()['redirect_path'] == 'https://www.twitch.tv/':
                    created += 1
                    token  = r.json()['access_token']
                    userId = r.json()['userID'] 
                    with open('Results/tokens.txt', 'a') as f:
                        f.write(f"{token}\n")
                    with open('Results/accounts.txt', 'a') as f:
                        f.write(f"{email}:{username}:{password}:{token}\n")
                    print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Generated  {token[0:25]}***** ({created})")

                else:
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Error")
    except Exception as e:
        print(e)


os.system('cls')
x = checkFormat()
if x == False:
    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Invalid Proxy Format")
else:
    threads = int(input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Threads: "))
    apikey  = input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Api key: ")
    for i in range(threads):
        threading.Thread(target=Gen, args=(apikey,)).start()
