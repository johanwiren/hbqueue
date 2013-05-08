hbqueue
=======

Queue Handbrake jobs with a web gui.

Usage
-----

Start the server 

    ./HandbrakeQueue &

Schedule some commands

    curl -d "/usr/bin/ping www.google.com" http://localhost:8000
    curl -d "/usr/bin/cat /etc/resolv.conf" http://localhost:8000

Check out the job status page on http://localhost:8000
