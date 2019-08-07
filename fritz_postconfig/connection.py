import requests
from .error import *
from xml.etree import ElementTree as ET



LOCATION_DICT = {
    'wlan': 'monitor',
    'internet': 'pppoe',
    'system': 'reset',
    'home': 'home',
}

class Connection:
    def __init__(self, host):
        self.host = host
        self._sid = None
    def call_api(self, route, data):
        if not self._sid is None:
            data['sid'] = self._sid
        resp = requests.post(self.host + route, data=data)
        return resp
    def request(self, route, data={}, getpage='../html/de/menus/menu2.html'):
        req_dict = dict()
        req_dict.update({
            'getpage': getpage,
            #'errorpage': errorpage,
            'var:pagename': LOCATION_DICT[route],
            #'var:errorpagename': LOCATION_DICT[route],
            #'var:pagemaster': '',
            #'var:funknetze': '',
            #'var:uiAutoConfig': '',
            'var:menu': route,
        })
        req_dict.update(data)
        return self.call_api('/cgi-bin/webcm', data=req_dict)
    def reset(self):
        self.request(
            'system',
            data={
                'login:command/defaults': '../gateway/commands/saveconfig.html'
            },
            getpage='../html/restore.html'
        )
        self.request(
            'home',
            data={
                'login:command/defaults': '../gateway/commands/saveconfig.html'
            },
            getpage='../html/restore.html'
        )
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