from fritz_postconfig import Connection
from random import randint
import subprocess
import time
import re
import json


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
# Setup connection
fritz = Connection(host)
print('Sending reset request... ')
fritz.reset()
for remaining in range(100, 0, -1):
    print('\r', f'Waiting for reset, {remaining}s remaining...', end='')
    time.sleep(1)
fritz.login()

with open('7170.json') as file:
    json_data = json.load(file)

for config_info in json_data:
    print(config_info['description'], '...', end='')
    if config_info['method'] == 'call_api':
        fritz.call_api(config_info['route'], data=config_info['data'])
    else:
        fritz.request(config_info['route'], data=config_info['data'])
    print('DONE')

# Scrape MAC
expression = r'(?:(?:[0-9a-fA-F]){2}:){5}(?:[0-9a-fA-F]){2}'
resp = fritz.request('internet')
print(resp.text)
mac, *_ = re.findall(expression, resp.text)
print('MAC-Address: {}'.format(mac))
# configure wlan settings
data = {
    'wlan:settings/channel': randint(1, 10),
    'wlan:settings/power_level': '2',
}
pass

raise SystemExit

# Password temp
# 6a57e57f-cd5e23c3e5b7537fcc26dde56fa1011b
# Enable Expert mode
print('Enabeling expert mode... ')
fritz.call_api('/system/expert.lua', data={
    'expert': 1
})
print('DONE')
# configure internet settings
print('Configuring "internet"... ', end='', flush=True)
data = {
    # "providerlist:settings/activeprovider": "other",
    # "connection0:settings/type": "bridge",
    "connection0:settings/tcom_targetarch": "0",
    # "connection0:settings/aontv_arch": "0",
    "box:settings/ManualDSLSpeed": "0",
    "sar:settings/encapsulation": "dslencap_ether",
    "sar:settings/autodetect": "0",
    "sar:settings/VPI": "1",
    "sar:settings/VCI": "32",
    "sar:settings/dslencap_ether/use_dhcp": "1",
    "box:settings/ata_mode": "0",
    "var:ifmode": "modem",
}
resp = fritz.request('internet', data=data)
print('DONE')
input()
