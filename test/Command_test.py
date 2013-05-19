from command import Command

def command_test():
    c = Command(['/usr/bin/echo', 'test'])
    assert c.status == 'Queued'
    c.run()
    assert c.stdout == 'test\n'
