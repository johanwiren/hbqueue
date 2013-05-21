#!/usr/bin/env python

from Command import Command
from HttpHandler import HttpHandler
from Queue import Queue
from threading import Thread
from time import sleep
import BaseHTTPServer
import os
import sys
import yaml

class HandbrakeQueue(object):

    def __init__(self):
        self.BASEDIR = ('targets')
        self.OUTPUTDIR = ('output')
        self.DONEDIR = ('done')
        self.httpserver = HttpServer(('', 8000), HttpHandler, self)
        self.files = []
        self.commands = []
        self.q = Queue()
        self.run_threads = True
        self.threads = [Thread(target=self.runner), 
                Thread(target=self.scanner)]
        self.load_targets()
        self.create_target_dirs()
        self.ensure_dir_exists(self.BASEDIR) 
        self.ensure_dir_exists(self.OUTPUTDIR) 
        self.ensure_dir_exists(self.DONEDIR) 

    def ensure_dir_exists(self, directory):
        if ( os.path.exists(directory) and 
                os.path.isdir(directory) ):
            pass 
        else:
            os.mkdir(directory)

    def create_target_dirs(self):
        for target_dir in [ x['name'] for x in self.targets ]:
            self.ensure_dir_exists('%s/%s' % (self.BASEDIR, target_dir))

    def load_targets(self):
        try:
            f = open('targets.yml')
        except:
            print "Error: Targets file not found"
            sys.exit(1)
        try:
            self.targets = yaml.load(f.read())
        except:
            print "Error: Could not load targets file"
            sys.exit(1)
        self.targets_timestamp = os.stat(f.name).st_mtime
        f.close()

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
            for t in self.targets:
                target_dir = '/'.join([self.BASEDIR, t['name']])
                for f in [ x for x in os.listdir(target_dir) 
                        if x not in self.files ]: 

                    f_path = '/'.join([target_dir, f])
                    if f == '.DS_Store':
                        continue
                    self.files.append(f)
                    if f.upper().endswith('.ISO'):
                        out = '.'.join(f.split('.')[:-1])
                    out = '.'.join([out, t['extension']])
                    out_path = '/'.join([self.OUTPUTDIR, out])
                    if os.path.isfile(out_path):
                        continue
                    args = ['HandBrakeCLI']
                    args.extend(['-i', f_path])
                    args.extend(t['args'].split())
                    args.extend(['-o', out_path])
                    self.add(args)
            if os.stat('targets.yml').st_mtime > self.targets_timestamp:
                print 'Reloading targets'
                self.load_targets()
                self.create_target_dirs()
            sleep(1)

class HttpServer(BaseHTTPServer.HTTPServer):

    def __init__(self, address, handler, hbq):
        self.hbq = hbq
        BaseHTTPServer.HTTPServer.__init__(self, address, handler)

if __name__ == "__main__":
    HandbrakeQueue().run_server()
    

        
