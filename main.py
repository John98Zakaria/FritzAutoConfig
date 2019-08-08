from fritz_postconfig import Connection
from random import randint
import time
import subprocess
import json
import requests


def wait_for_connection(host):
    print('Waiting for Fritz!Box...', end='', flush=True)
    while True:
        returncode = subprocess.call('ping ' + host, stdout=subprocess.PIPE)
        if returncode == 0:
            break
        print('.', end='', flush=True)
        time.sleep(1)
    print('')


host = input('Please enter host ({ENTER} for fritz.box): ')
if not host:
    host = 'fritz.box'
wait_for_connection(host)
'<modelDescription>([\s\S])</modelDescription>'
host = 'http://' + host

# Detect fritzbox


# Setup connection


fritz = Connection(host, 'FRITZ!Box FON WLAN')
fritz.reset()
for i in range(100,-1,-1):
    print(f"\r restarting {i}s left",end="")
    time.sleep(1)

print()

fritz.enableExpertMode()
fritz.setupInternet()
fritz.login()

fritz.wifiSetup()