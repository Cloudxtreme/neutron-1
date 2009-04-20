#$ neutron_plugin 01

import wsgiserver
#
# used example from wsgiserver as template
# (c) 2006-2007 Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com

# this plugin can provide huge possibilities for almost 
# all needs, later this can be powered with AJAX and Prototype,
# and some c00l css.
# if you miss something - extend this :)

listen_addr = 'localhost'
listen_port = 12345
server_name = 'localhost'

HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.timestamp {color: #AAAAAA;}
.system {color: #009900; font-weight: bold;}
.emote {color: #AA0099;}
.self {color: #CC0000;}
.normal {color: #0000AA;}
h1 { color: #336699; font-family: sans-serif; border-bottom: #224466 solid 3pt; letter-spacing: 3px; margin-left: 20pt; }
h2 { color: #663399; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a { margin-left: 20pt; margin-right: 20pt; font-family: arial,helvetica; font-weight: bold; color: #0D0D0D; }
//-->
</style>
<title>Welcome to Neutron Web Server</title>
</head>
<body>
<div style="color: #AAAAAA; text-align: right; font-family: monospace; letter-spacing: 3px">neutron web server</div> """


FOOTER =  """<hr><div align="center"><font color="#990000">[ Script Execution time: %s ]</font></div></body>
</html>
"""

REDIRECTOR = """<html>
<head>
<title></title>
<meta http-equiv="Refresh" content="0; URL=/index.html">
<style></style>
</head>
<body>
</body>
</html>"""

INDEXD = """
<div align="center">
<a href="/plugins.html">Plugins</a>|<a href="/status.html">Status</a>|<a href="/roster.html">Roster</a>
|<a href="/rooms.html">Rooms</a>|<a href="/commands.html">Commands</a>|<a href="/logs.html">Logs</a>
|<a href="/access.html">Access</a>
</div>"""

def exec_time(timestamp):
    return str(time.time() - timestamp)[:6]
    
def index_page(environ, start_response):
    global HEADER
    global FOOTER
    global INDEXD
    start_stamp = time.time()
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    time.sleep(0.01)
    data = HEADER + INDEXD + FOOTER%exec_time(start_stamp)
    return data

def index_redir(environ, start_response):
    global REDIRECTOR
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    data = REDIRECTOR
    return data

# from plugin_plugin.py
def list_plugins(environ, start_response):
	global HEADER
	global FOOTER
	global INDEXD
	start_stamp = time.time()
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
	plugins_count = 0
	valid_plugins = find_plugins()
	total_plugins = len(valid_plugins)
	reply = '\nAvailable Neutron Plugins(stripped names, suitable for using !loadpl):\n'
	for plugin in valid_plugins:
	    reply += plugin.split('_plugin.py')[0] + '\n'
	reply += 'Total plugins: ' + str(total_plugins)
	time.sleep(0.01)
	data = HEADER + INDEXD + '<pre>' + reply + '</pre>' + FOOTER%exec_time(start_stamp)
	return data
	
# from admin_plugin.py
def display_status(environ, start_response):
	global HEADER
	global FOOTER
	global INDEXD
	start_stamp = time.time()
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
	initialize_file('crash.log','')
	crashdata = read_file('crash.log')
	if crashdata.strip():
	    crashdata = 'Last crashlog:\n\n' + crashdata
	# from modules/iq.py
	uname=os.popen("uname -sr", 'r')
	osver=uname.read().strip()
	uname.close()
	uname=os.popen("uname -mp", 'r')
	machver=uname.read().strip()
	uname.close()
	python_ver = 'Python: ' + sys.version.split(' ')[0]
	osver = osver + ' ' + python_ver + ' on ' + machver
	# end
	time.sleep(0.01)
	data = HEADER + INDEXD + '<br>Running using: <b>%s</b></br><pre>'%osver + crashdata + '</pre>' + FOOTER%exec_time(start_stamp)
	return data

def commands_page(environ, start_response):
	global HEADER
	global FOOTER
	global INDEXD
	start_stamp = time.time()
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
	source = ['none@jabber.org','/Client']
	# from help_plugin.py
	commandlist = []
	for command in COMMANDS.keys():
    	    if has_access(source, COMMANDS[command]['access']):
        	commandlist.append(command)
	commandlist.sort()
	# end
	reply = '<br>\n'.join(commandlist)
	time.sleep(0.01)
	data = HEADER + INDEXD +'<br>' + reply + FOOTER%exec_time(start_stamp)
	return data

def rooms_page(environ, start_response):
	global HEADER
	global FOOTER
	global INDEXD
	start_stamp = time.time()
	status = '200 OK'
	response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
        reply = '<br>\nTotal Rooms: '+ str(len(groupchats)) + '<br>\n' + '<br>\n'.join(groupchats)
	time.sleep(0.01)
	data = HEADER + INDEXD +'<br>' + reply + FOOTER%exec_time(start_stamp)
	return data

wsgi_apps = [('/', index_redir), ('/index.html', index_page), ('/plugins.html', list_plugins),
	     ('/status.html', display_status), ('/commands.html', commands_page),
	     ('/rooms.html', rooms_page), ('/logs.html', index_page), ('/roster.html',index_page),
	     ('/access.html', index_page)
	    ]

server = wsgiserver.CherryPyWSGIServer((listen_addr, listen_port), wsgi_apps,
                                           server_name=server_name)

def starter():
    try:
	print printc(color_bright_blue, 'Starting Neutron Web Server(%s): '%server_name + listen_addr + ':' + str(listen_port))
        server.start()
    except:
        server.stop()
    
if __name__ == '__main__':
	thread.start_new(starter,())