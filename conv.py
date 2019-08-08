data = '''errorpage: ../html/de/menus/menu2.html
var:pagename: common
var:errorpagename: common
var:menu: wlan
var:pagemaster: 
time:settings/time: 1565222221,-120
var:devid: 
wlan:settings/ap_enabled: 1
wlan:settings/ssid: Dontea
wlan:settings/hidden_ssid: 0
wlan:settings/user_isolation: 1
wlan:settings/is_macfilter_active: 0
ctlusb:settings/autoprov_enabled: 0
wlan:settings/wireless_stickandsurf_enabled: 0
mini:settings/enabled: 0'''
data = dict(name.rsplit(': ', maxsplit=1) for name in data.splitlines())
for name in data:
    print('"{}": "{}",'.format(name, data[name]))