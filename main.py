from fritz_postconfig import Connection
import re
import requests
import time



NAME_DICT = {
    '7141': 'Fritz!Box Fon WLAN 7141 (UI)',
    '7170': 'Fritz!Box Fon WLAN 7170 (UI)',
    'default': 'Fritz!Box Fon WLAN 7141 (UI)',
}

def main():
    host = input('Please enter host ({ENTER} for fritz.box): ')
    if not host:
        host = '192.168.178.1'
    host = 'http://' + host
    # initialize connection
    fritz = Connection(host)
    print('Please enter one of the following modelnames: ')
    for name in NAME_DICT:
        print('- {:>10}'.format(name))
    modelname = input('> ')
    if not fritz.wait_for_connection():
        print('It is dead, Jim...')
        return
    if modelname in NAME_DICT:
        modelname = NAME_DICT[modelname]
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
                for name in NAME_DICT:
                    if name in modelname:
                        modelname = NAME_DICT[name]
                        break
                else:
                    modelname = None
                break
        print(' DONE')
    # Manual model entry
    if modelname is None:
        print('error finding modelname, using default')
        modelname = NAME_DICT['default']
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
            main()
        except KeyboardInterrupt:
            raise SystemExit
        except Error as e:
            print(e)