data = '''getpage: ../html/restore.html
errorpage: ../html/de/menus/menu2.html
var:lang: de
var:pagename: reset
var:errorpagename: reset
var:menu: system
var:pagemaster: 
time:settings/time: 
var:tabReset: 1
logic:command/defaults: ../gateway/commands/saveconfig.html'''
data = dict(name.rsplit(': ', maxsplit=1) for name in data.splitlines())
for name in data:
    print('"{}": "{}",'.format(name, data[name]))