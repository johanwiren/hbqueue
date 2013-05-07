import subprocess
import threading

class Command(threading.Thread):

    def __init__(self, args):

        threading.Thread.__init__(self)
        self.stdout = ''
        self.args = args
        self.process = None
        self.start()

    def run(self):
        self.process = subprocess.Popen(
            self.args, 
            bufsize=1, 
            shell=False,
            stdout=subprocess.PIPE)

        for line in iter(self.process.stdout.readline, ""):
            self.stdout += line

        self.process.communicate()

    
