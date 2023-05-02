import os
import re
import time
import random
import string
import requests
import threading

from os        import system
from os.path   import isfile, join
from colorama  import Fore



class stats:
    created = 0
    errors  = 0 

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
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Failed to return a Kasada Solve Error")
                    return False
        except:
            pass

class MailGW:
    def __init__(self):
        self.base_url = 'https://api.mail.gw'
        self.domain   = self.get_domain() 

    def get_domain(self):
        return requests.get(self.base_url + '/domains').json()['hydra:member'][0]['domain']

    def get_email(self):
        try:
            json = {
                'address' : f"{''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxzPOIUYTREWQMNBVCXZLKJHGFDSA0987654321', k=12))}@{self.domain}",
                'password': ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxzPOIUYTREWQMNBVCXZLKJHGFDSA0987654321', k=14))
            }
            x = requests.post(self.base_url + '/accounts', json=json).json()
            return (x['id'], x['address'], json['password'])
        except:
            return False
    
    def get_token(self, email, password):
        try:
            json = {
                'address' : email,
                'password': password
            }
            return requests.post(self.base_url + '/token', json=json).json()['token']
        except:
            return False
    
    def get_messages(self, token):
        try:
            while True:
                time.sleep(2)
                x = requests.get(self.base_url + f'/messages', headers={'Authorization': f'Bearer {token}'})
                if 'subject' in x.text:
                    subject = x.json()['hydra:member'][0]['subject']
                    return subject[:6]
        except:
            return False

class twitch:
    def __init__(self) -> None:
        self.session = requests.Session()

    def get_format(self) -> bool:
        pattern = r'^(?:(?P<user>[^:@]+):(?P<pass>[^:@]+)@)?(?P<host>[^:]+):(?P<port>\d+)$'
        proxies = open('data/proxies.txt', 'r').read().splitlines()
        for proxy in proxies:
            match = re.match(pattern, proxy)
            if match:
                return True
            else:
                return False

    def get_username(self) -> str:
        try:
            with self.session as session:
                username = session.get('https://names.drycodes.com/10').json()[0]
                headers  = {
                    'Accept'            : '*/*',
                    'Accept-Language'   : 'en-GB',
                    'Client-Id'         : 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                    'Connection'        : 'keep-alive',
                    'Content-Type'      : 'text/plain;charset=UTF-8',
                    'Origin'            : 'https://www.twitch.tv',
                    'Referer'           : 'https://www.twitch.tv/',
                    'Sec-Fetch-Dest'    : 'empty',
                    'Sec-Fetch-Mode'    : 'cors',
                    'Sec-Fetch-Site'    : 'same-site',
                    'User-Agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                    'sec-ch-ua'         : '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    'sec-ch-ua-mobile'  : '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                json = [{
                    "operationName": "UsernameValidator_User",
                    "variables": {
                    "username" : username
                    },
                    "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660"
                    }
                    }
                    }]
                response = session.post('https://gql.twitch.tv/gql', json=json, headers=headers).json()[0]['data']['isUsernameAvailable']
                if response == True:
                    return username
                else:
                    return username + ''.join(random.choices('poiuytrewqlkjhgfdsaamnbvcxz', k=3))
        except:
            return ''.join(random.choices('poiuytrewqlkjhgfdsaamnbvcxz', k=10))

    def get_data(self) -> tuple:
        username = self.get_username()
        password = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz0987654321', k=12))
        email    = ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz0987654321', k=10)) + random.choice(['@outlook.com', '@gmail.com', '@yahoo.com'])
        proxy    = random.choice(open('data/proxies.txt', 'r').read().splitlines())
        return (username, password, email, proxy)
    
    def get_token(self, proxy: str, apikey) -> str:
        try:
            with requests.Session() as session:
                kas = captchaio(apikey).createTask(proxy)
                if kas == False:
                    pass
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
            return False

    def changeBio(self, token: str, userId: str) -> None:
        try:
            with self.session as session:
                quote = session.get('https://api.quotable.io/random').json()['content']
                headers = {"accept": "application/vnd.twitchtv.v3+json","accept-encoding": "gzip","accept-language": "en-us","api-consumer-type": "mobile; Android/1403020","authorization": f"OAuth {token}","client-id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp","connection": "Keep-Alive","content-type": "application/json","host": "gql.twitch.tv","user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020","x-apollo-operation-id": "14396482e090e2bfc15a168f4853df5ccfefaa5b51278545d2a1a81ec9795aae","x-apollo-operation-name": "UpdateUserDescriptionMutation","x-app-version": "14.3.2",}
                json = [
                {
                    "operationName": "UpdateUserDescriptionMutation",
                    "variables": {
                    "userID": userId,
                    "newDescription": quote
                    },
                    "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "14396482e090e2bfc15a168f4853df5ccfefaa5b51278545d2a1a81ec9795aae"
                    }
                    }
                }
                ]
                response = self.session.post('https://gql.twitch.tv/gql', json=json, headers=headers).json()[0]['data']['updateUser']['error']
                if response is None:
                    print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Updated Bio {token[0:25]}*****")
                else:
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Failed to Change Bio {token[0:25]}*****")
        except:
            pass

    def createUpload(self, token: str, userID: str) -> str:
        try:
            with self.session as session:
                headers = {"accept": "application/vnd.twitchtv.v3+json","accept-encoding": "gzip","accept-language": "en-us","api-consumer-type": "mobile; Android/1403020","authorization": f"OAuth {token}","client-id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp","connection": "Keep-Alive","content-type": "application/json","host": "gql.twitch.tv","user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020","x-apollo-operation-id": "4de617743abe2fedc733c0be56f435fc2ecb6f06d34ab1d0a44e9350a232190b","x-apollo-operation-name": "CreateProfileImageUploadURL","x-app-version": "14.3.2",}
                json = [
                {
                    "operationName": "CreateProfileImageUploadURL",
                    "variables": {
                    "input": {
                        "format": "PNG",
                        "userID": userID
                    }
                    },
                    "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "4de617743abe2fedc733c0be56f435fc2ecb6f06d34ab1d0a44e9350a232190b"
                    }
                    }
                }
                ]
                return session.post('https://gql.twitch.tv/gql', json=json, headers=headers).json()[0]['data']['createProfileImageUploadURL']['uploadURL']
        except:
            pass

    def sendUpload(self, token: str, userId: str) -> None:
        try:
            with self.session as session:
                headers  = {"accept": "application/vnd.twitchtv.v3+json","accept-encoding": "gzip","accept-language": "en-us","api-consumer-type": "mobile; Android/1403020","client-id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp","connection": "Keep-Alive","content-length": "1777","content-type": "application/octet-stream","host": "twitchuploadservice-infra-prod-us-ingest4069586c-608wwzuuil7q.s3-accelerate.amazonaws.com","user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020","x-app-version": "14.3.2",}
                rand_pic = random.choice([f for f in os.listdir("data/avatars/") if isfile(join("data/avatars/", f))])
                data     = open(f'data/avatars/{rand_pic}', 'rb')
                session.put(self.createUpload(token, userId), data=data, headers=headers)
                print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Updated Profile Image {token[0:25]}*****")
        except Exception as e:
            pass

    def verify(self, email, token, userId, code):
        try:
            deviceId = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            headers = {"accept": "application/vnd.twitchtv.v3+json","accept-encoding": "gzip","accept-language": "en-us","api-consumer-type": "mobile; Android/1403020","authorization": f"OAuth {token}","client-id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp","connection": "Keep-Alive","content-type": "application/json","host": "gql.twitch.tv","user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020) tv.twitch.android.app/14.3.2/1403020","x-apollo-operation-id": "72babafce68ab9862b6e4067385397b5d70caf4c2b45566970f57e5184411649","x-apollo-operation-name": "ValidateVerificationCode","x-app-version": "14.3.2","x-device-id": deviceId}
            json = [
            {
                "operationName": "ValidateVerificationCode",
                "variables": {
                "input": {
                    "address": email,
                    "code"   : code,
                    "key"    : userId
                }
                },
                "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "72babafce68ab9862b6e4067385397b5d70caf4c2b45566970f57e5184411649"
                }
                }
            }
            ]
            response = requests.post('https://gql.twitch.tv/gql', json=json, headers=headers)
            if response.json()[0]['data']['validateVerificationCode']['request']['status'] == 'VERIFIED':
                print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Email Verified {token[0:25]}*****")
            else:
                print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Failed to verify email")
        except:
            print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Failed to verify email [-1]")

    def Gen(self, apikey: str) -> None:
        try:
            with self.session as session:
                username, password, emaill, proxy = self.get_data()
                id, email, epassword = MailGW().get_email()
                if not email:
                    email = emaill
                    etoken = False
                else:
                    etoken = MailGW().get_token(email, epassword)
                integrity = self.get_token(proxy, apikey)
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
                            "year" : random.randint(1960,2005)
                        },
                        "client_id"                : "kd1unb4b3q4t58fwlpcbzcbnm76a8fp",
                        "email"                    : email,
                        "include_verification_code": True,
                        "integrity_token"          : integrity,
                        "password"                 : password,
                        "username"                 : username
                    }
                    r = session.post('https://passport.twitch.tv/protected_register', json=json, headers=headers, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
                    if r.json()['redirect_path'] == 'https://www.twitch.tv/':
                        stats.created += 1
                        token  = r.json()['access_token']
                        userID = r.json()['userID'] 
                        with open('data/Results/tokens.txt', 'a') as f:
                            f.write(f"{token}\n")
                        with open('data/Results/accounts.txt', 'a') as f:
                            f.write(f"{email}:{username}:{password}:{token}\n")
                        print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Generated {token[0:25]}***** ({stats.created})")
                        self.changeBio(token, userID)
                        self.sendUpload(token, userID)
                        if etoken != False:
                            code = MailGW().get_messages(etoken)
                        self.verify(email, token, userID, code)
                    else:
                        print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Error")
        except Exception as e:
            print(e)


system('cls')
if twitch().get_format() == False:
    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Invalid Proxy Format\n Use user:pass@host:port")
else:
    threads = int(input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Threads: "))
    apikey  = input(f"{Fore.BLUE}[ {Fore.YELLOW}> {Fore.BLUE}]{Fore.RESET} Api key: ")
    for i in range(threads):
        threading.Thread(target=twitch().Gen, args=(apikey,)).start()
