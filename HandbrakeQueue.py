#!/usr/bin/env python

from command import Command
import BaseHTTPServer
from httphandler import HttpHandler

class HandbrakeQueue(object):

    def __init__(self):
        self.commands = []

    def add(self, args):
        self.commands.append(Command(args))

    def run_server(self):
        self.httpserver = HttpServer(('', 8000), HttpHandler, self)
        self.httpserver.serve_forever()

class HttpServer(BaseHTTPServer.HTTPServer):

    def __init__(self, address, handler, hbq):
        self.hbq = hbq
        BaseHTTPServer.HTTPServer.__init__(self, address, handler)

if __name__ == "__main__":
    hbq = HandbrakeQueue()
    hbq.run_server()
