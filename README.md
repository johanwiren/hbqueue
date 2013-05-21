hbqueue
=======

Queue Handbrake jobs with a web gui.

Configuration
-------------

Create a `target.yml` containing your encoding targets and their respective HandBrake arguments:
```
---
- name: AppleTV
  args: -Z AppleTV -N sve
  extension: m4v
```

Usage
-----

Start the server 

    ./HandbrakeQueue.py

Drop your media files in `targets/AppleTV` and check out the job status page on http://localhost:8000
