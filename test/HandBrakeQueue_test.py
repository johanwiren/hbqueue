from HandbrakeQueue import HandbrakeQueue

def handbrakequeue_test():
    hbq = HandbrakeQueue()
    c = hbq.add(['/usr/bin/sleep', '1'])
    assert c.status == 'Queued'
    c.run()
    assert c.status == 'Completed'
    c = hbq.add(['/usr/bin/echo', 'testrun'])
    c.run()
    assert c.stdout == 'testrun\n'

