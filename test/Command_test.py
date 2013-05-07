from command import Command

def command_test():
    c = Command(['/usr/bin/echo', 'test'])
    c.join()
    assert c.stdout == 'test\n'
