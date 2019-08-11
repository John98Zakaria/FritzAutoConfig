from fritz_postconfig import Connection
import time
import subprocess
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
host = 'http://' + host
# Detect fritzbox model
resp = requests.get(host + ':49000/tr64desc.xml')
result = re.findall('<modelName>(.*?)<\/modelName>', resp.text)
modelname, *_ = result
# Setup connection
fritz = Connection(host, modelname)
# reset
fritz.reset()
for i in range(100,-1,-1):
    print(f"\r restarting {i:>3}s left", end="")
    time.sleep(1)
print()
fritz.enableExpertMode()
fritz.setupInternet()
fritz.login()
fritz.wifiSetup()
