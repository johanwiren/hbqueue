#!/usr/bin/env python

from command import Command
from threading import Thread
import BaseHTTPServer
from httphandler import HttpHandler
from Queue import Queue

class HandbrakeQueue(object):

    def __init__(self):
        self.commands = []
        self.q = Queue()
        self.runner_thread = Thread(target=self.runner).start() 

    def runner(self):
        while True:
            command = self.q.get()
            command.start()
            command.join()

    def add(self, args):
        command = Command(args)
        self.commands.append(command)
        self.q.put(command)
        return command

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
