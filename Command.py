import distutils.spawn 
import os.path
import subprocess

class Command(object):

    def __init__(self, args):

        self.status = "Queued"
        self.stdout = ''
        if not os.path.isabs(args[0]):
            abspath = distutils.spawn.find_executable(args[0])
            args[0] = abspath
        self.args = args
        self.process = None

    def pause(self):
        self.process.send_signal(19)

    def resume(self):
        self.process.send_signal(18)

    def terminate(self):
        self.process.terminate()

    def kill(self):
        self.process.kill()

    def wait(self):
        self.process.wait()

    def run(self):
        print "Starting command %s" % self.args
        self.status = "Running"
        self.process = subprocess.Popen(
            self.args, 
            bufsize=1, 
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,)

        for line in iter(self.process.stdout.readline, ""):
            self.stdout += line

        self.process.wait()
        if self.process.returncode == 0:
            self.status = "Completed"
        else:
            self.status = "Failed"
        print "Job %s status: %s" % (self.args, self.status)
