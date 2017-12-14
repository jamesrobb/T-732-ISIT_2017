#!/usr/bin/python3
import sys

from flipflop import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from pictureframe_server import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
