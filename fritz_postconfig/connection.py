import requests
from .error import *
from xml.etree import ElementTree as ET
import json
import requests
import time
from random import randint

class Connection:
    def __init__(self, host, model=None):
        self.host = host
        self._sid = None
        self.model = model
        with open(self.model + '.json', 'r') as f:
            self.json = json.load(f)

    def call_api(self, dict):
        data = dict['data']
        route = dict['route']
        if not self._sid is None:
            data['sid'] = self._sid
        resp = requests.post(self.host + route, data=data)
        return resp

    def reset(self):
        # Assume Pass
        print("Resetting Router")
        relevantDict = self.json['resetWhenPass']
        requests.post(self.host + relevantDict['route'], data=relevantDict['data'])
        time.sleep(5)  # Wait before assuming no Pass
        # try:
        #     r = requests.get(self.host)
        # except requests.exceptions.ConnectionError:
        #     #Router was restarting, skip next step
        #     return
        # print("Router had no password, trying alternative")
        # relevantDict = self.json['restWhenNoPass']
        # self.call_api(relevantDict)

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
        wifiName = input("Wifi Namen eingeben")
        relevantDict['data']['wlan:settings/ssid']=wifiName
        wifiChannel = randint(1,11)
        relevantDict['data']['wlan:settings/channel'] = wifiChannel
        self.call_api(relevantDict)

    def login(self):
        resp = requests.get(self.host + '/login_sid.lua')
        if resp.ok:
            root = ET.fromstring(resp.text)
            self._sid = root.find('SID').text
        """
            if self._sid == '0000000000000000':
                return False
            else:
                return True
        else:
            return True
        """
