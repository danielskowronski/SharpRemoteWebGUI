#!/usr/bin/python3
from wsgiref.simple_server import make_server
from tg import MinimalApplicationConfigurator,TGController,request,expose
import subprocess, re

keepalive_path="/tmp/sharp_keepalive.txt"

def sendToSharp(key):
	rc = subprocess.call(["/usr/bin/irsend", "SEND_ONCE", "sharp", re.sub(r"\W+", "", key)])
	return rc

class RootController(TGController):
	@expose(content_type='text/html')
	def index(self):
		file = open("./index.html","r") 
		return file.read() 
	@expose(content_type='application/json')
	def send(self, *args):
		rc=sendToSharp(args[0])
		return '{"cmd":"'+args[0]+'", "error":"'+str(rc)+'"}'
	@expose(content_type='application/json')
	def keepalive(self):
		try:
			f=open(keepalive_path,"r")
			contents=f.read()
			f.close()
			if "enable" in contents:
				rc = 0
				rc+= sendToSharp("down")
				rc+= sendToSharp("up")
			else:
				rc=-1
		except:
			rc=-1
		return '{"cmd":"keepalive", "error":"'+str(rc)+'"}'
	@expose(content_type='application/json')
	def setkeepalive(self, *args):
		try:
			f=open(keepalive_path,"w")
			if args[0]=="enable":
				f.write("enable")
			else:
				f.write("disable")
			f.close()
			rc=0
		except:
			rc=1
		return '{"cmd":"setkeepalive", "error":"'+str(rc)+'"}'

config = MinimalApplicationConfigurator()
config.update_blueprint({
	'root_controller': RootController()
})
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()