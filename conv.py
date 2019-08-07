data = '''getpage: ../html/restore.html
errorpage: ../html/restoreerror.html
var:lang: <? echo $var:lang ?>
var:pagename: home
var:menu: home
login:command/defaults: ../gateway/commands/saveconfig.html'''
data = dict(name.rsplit(': ', maxsplit=1) for name in data.splitlines())
for name in data:
    print('"{}": "{}",'.format(name, data[name]))