#!/usr/bin/python3
from wsgiref.simple_server import make_server
from tg import MinimalApplicationConfigurator,TGController,request,expose
import subprocess, re

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

config = MinimalApplicationConfigurator()
config.update_blueprint({
	'root_controller': RootController()
})
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()