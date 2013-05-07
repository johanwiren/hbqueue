from HandbrakeQueue import HandbrakeQueue

def handbrakequeue_test():
    hbq = HandbrakeQueue()
    hbq.add(['/usr/bin/sleep', '1'])
    assert hbq.commands[0].is_alive()
    hbq.add(['/usr/bin/echo', 'testrun'])
    hbq.commands[1].join()
    assert hbq.commands[1].stdout == 'testrun\n'

