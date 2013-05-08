from SimpleHTTPServer import SimpleHTTPRequestHandler
import json
import re

class HttpHandler(SimpleHTTPRequestHandler):

    def do_GET(s):
        job = re.compile('^/jobs/[0-9]+$')
        joblist = re.compile('^/jobs/?$')
        if job.match(s.path):
            s.send_response(200)
            s.send_header('Content-Type:', 'application/json')
            s.end_headers()
            id = int(s.path.split('/')[2])
            result = dict()
            result['command'] = " ".join(s.server.hbq.commands[id].args)
            result['alive'] = s.server.hbq.commands[id].is_alive()
            result['stdout'] = s.server.hbq.commands[id].stdout
            s.wfile.write(json.dumps(result))
        elif joblist.match(s.path):
            s.send_response(200)
            s.send_header('Content-Type:', 'application/json')
            s.end_headers()
            result = dict()
            for i, cmd in enumerate([[x.args, x.is_alive()] for x in s.server.hbq.commands]):
                result[i] = dict(command=" ".join(cmd[0]), alive=cmd[1])
            s.wfile.write(json.dumps(result))
        else:
            SimpleHTTPRequestHandler.do_GET(s)

    def do_POST(s):
        command = s.rfile.read(int(s.headers['Content-Length']))
        s.server.hbq.add(command.split())
        s.send_response(200)
        s.end_headers()
