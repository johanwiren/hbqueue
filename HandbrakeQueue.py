#!/usr/bin/env python

from command import Command
from httphandler import HttpHandler
from Queue import Queue
from threading import Thread
import BaseHTTPServer
import os
from time import sleep

class HandbrakeQueue(object):

    def __init__(self):
        self.httpserver = HttpServer(('', 8000), HttpHandler, self)
        self.files = []
        self.commands = []
        self.q = Queue()
        self.run_threads = True
        self.threads = [Thread(target=self.runner), 
                Thread(target=self.scanner)]

    def runner(self):
        while self.run_threads:
            command = self.q.get()
            if command != 'stop_server':
                command.run()

    def add(self, args):
        command = Command(args)
        self.commands.append(command)
        self.q.put(command)
        return command

    def stop_server(self):
        self.run_threads = False
        self.q.put('stop_server')
        for t in self.threads:
            t.join()

    def run_server(self):
        for t in self.threads:
            t.start()
        try:
            self.httpserver.serve_forever()
        except KeyboardInterrupt:
            self.stop_server()

    def scanner(self):
        while self.run_threads:
            if os.path.isdir('targets'):
                for t in [ x for x in os.listdir('targets') 
                        if os.path.isdir('targets/%s' % x) ]:
                    for f in [ x for x in os.listdir('targets/' + t) 
                            if x not in self.files ]:
                        if f == '.DS_Store':
                            continue
                        self.files.append(f)
                        if f.upper().endswith('.ISO'):
                            f = '.'.join(f.split('.')[:-1])
                        f = '%s.m4v' % f
                        if os.path.isfile('output/%s' % f):
                            continue
                        args = ['HandBrakeCLI']
                        args.extend(['-i', 'targets/%s/%s' % (t,f)])
                        args.extend(t.split())
                        args.extend(['-o', 'output/%s' % f])
                        self.add(args)
            sleep(1)

class HttpServer(BaseHTTPServer.HTTPServer):

    def __init__(self, address, handler, hbq):
        self.hbq = hbq
        BaseHTTPServer.HTTPServer.__init__(self, address, handler)

if __name__ == "__main__":
    HandbrakeQueue().run_server()
    

        
