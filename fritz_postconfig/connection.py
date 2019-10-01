import requests
from .error import *
from xml.etree import ElementTree as ET
import json
import requests
import time
import re
import subprocess
import urllib
from random import randint

class Connection:
    def __init__(self, host, model=None):
        self.host = host
        self._sid = None
        self.model = model

    def setup(self, *args):
        with open(self.model + '.json', 'r') as f:
            self.json = json.load(f)
        if not self.reset():
            # reset failed, retry with different model
            return False
        self.login()
        self.enableExpertMode()
        self.setupInternet()
        self.wifiSetup()
        self.getMac()
        return True

    def call_api(self, dict):
        data = dict['data']
        route = dict['route']
        if not self._sid is None:
            data['sid'] = self._sid
        resp = self._request(self.host + route, data=data)
        return resp

    def wait_for_connection(self, path=''):
        print('Waiting for Fritz!Box...', end='', flush=True)
        start_time = time.time()
        while True:
            try:
                requests.get(self.host)
            except:
                pass
            else:
                break
            print('.', end='', flush=True)
            time.sleep(1)
        print('')
        end_time = time.time()
        return (end_time - start_time) < (3*60)

    def wait_for_reset(self, path=''):
        print('Waiting for Fritz!Box reset: ', end='', flush=True)
        start_time = time.time()
        while True:
            try:
                requests.get(self.host)
            except:
                break
            print('-', end='', flush=True)
            delta = time.time() - start_time
            if delta > 20:
                print()
                return False
            time.sleep(1)
        print('_', end='', flush=True)
        while True:
            try:
                requests.get(self.host)
            except:
                pass
            else:
                break
            print('_', end='', flush=True)
            time.sleep(1)
        print('-')
        return True

    def reset(self):
        # Assume Pass
        print("Resetting Router")
        relevantDict = self.json['resetWhenPass']
        self._request(self.host + relevantDict['route'], data=relevantDict['data'])
        if self.wait_for_reset():
            return True
        print("Router had no password, trying alternative")
        relevantDict = self.json['restWhenNoPass']
        self.call_api(relevantDict)
        return self.wait_for_reset()

    def _request(self, *args, **kwargs):
        #try:
        return requests.post(*args, **kwargs)
        #except:
        #    pass

    def enableExpertMode(self):
        self.login()
        print('Activating expert mode')
        relevantDict = self.json['enableExpertMode']
        self.call_api(relevantDict)

    def setupInternet(self):
        print("Setting up internet settings")
        relevantDict = self.json['setupInternet']
        self.call_api(relevantDict)

    def wifiSetup(self):
        print("Setting up Wifi Settings")
        relevantDict = self.json['wifiSetup']
        wifiName = input("Wifi Namen eingeben: ")
        relevantDict['data']['wlan:settings/ssid'] = wifiName
        wifiChannel = randint(1, 11)
        relevantDict['data']['wlan:settings/channel'] = wifiChannel
        self.call_api(relevantDict)

    def getMac(self):
        route = '/cgi-bin/webcm'
        query = {
            'getpage': '../html/de/menus/menu2.html',
            'var:lang': 'de',
            'var:menu': 'internet',
            'var:pagename': 'pppoe',
            'var:activtype': 'bridge'
        }
        if not self._sid is None:
            query['sid'] = self._sid
        resp = requests.get(self.host + route, params=query)
        findings = re.findall('((?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2})', resp.text)
        findings, *_ = findings
        print(findings)

    def login(self):
        resp = requests.get(self.host + '/login_sid.lua')
        if resp.ok:
            root = ET.fromstring(resp.text)
            self._sid = root.find('SID').text
