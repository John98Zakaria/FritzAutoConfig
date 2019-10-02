from fritz_postconfig import Connection
import json
import re
import requests
import time



def main(config):
    host = input('Please enter host ({ENTER} for fritz.box): ')
    if not host:
        host = '192.168.178.1'
    host = 'http://' + host
    # initialize connection
    fritz = Connection(host)
    print('Please enter one of the following modelnames: ')
    for name in config:
        print('- {:>10}'.format(name))
    modelname = input('> ')
    if not fritz.wait_for_connection():
        print('It is dead, Jim...')
        return
    if modelname in config:
        modelname = config[modelname]
    else:
        # Detect fritzbox model
        print('Reading desc.xml-files...', end='', flush=True)
        modelname = None
        time.sleep(10)
        for file in ('/tr64desc.xml', '/igddesc.xml'):
            resp = requests.get(host + ':49000' + file)
            print(resp.text)
            if resp.ok:
                result = re.findall('<modelName>(.*?)<\/modelName>', resp.text)
                modelname, *_ = result
                for name in config:
                    if name in modelname:
                        modelname = config[name]
                        break
                else:
                    modelname = None
                break
        print(' DONE')
    # Manual model entry
    if modelname is None:
        print('error finding modelname, using default')
        modelname = config['default']
    # Call setup from connection
    print('Trying model "{}"...'.format(modelname))
    fritz.model = modelname
    if fritz.setup():
        print('Setup correctly')
        return
    print('Setup failed')

if __name__ == '__main__':
    while True:
        try:
            with open('config.json', 'r') as config:
                config = json.load(config)
            main(config)
        except KeyboardInterrupt:
            raise SystemExit
        except Exception as e:
            print(e)
