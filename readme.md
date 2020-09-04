# Event Tornado is a simple server-side solution for reflecting active terminal sessions 

Let's say you run a script (workflow) on some remote resource (docker/CI) where you limited/not able to see realtime logs of your workflow.
This solution can help you to see live logging.
You can stream your output (STDERR/STDOUT) and catch it using this approach.

## Server side

Make sure you have all dependencies installed `requirements.txt`

Just run `server.py`

### Example of install
```shell script
python3 -m venv venv
venv/bin/pip install -r requirements.txt
mkdir events
venv/bin/python server.py
```

Your log files will be collected to ``events`` folder

## Client side
You need to add following code to your script to be able to send output logs to the server...

You have 2 options:

- Option #1 is zero dependencies, tho quite dangerous since if you have networking issues or 
your network goes entirely down you are screwed because the named pipe blocks ``tee``, your output will be blocked and pretty much everything just hung
```shell script
[[ ! -p event_server ]] && mkfifo event_server
nc localhost 8888 <event_server &
ABSOLUTE_PIPE_PATH="$(readlink -e event_server)"
exec 1> >(tee "${ABSOLUTE_PIPE_PATH}") 2>&1
```

- Option #2 solves the issue above, tho instead of ``tea``, you need to use 
non-standard cli tool ``bftee`` (source code is in ``bftee.c``), which easily handles 
networking issues. It has its own buffer, and if the buffer is full (~ 16MB) in case of some 
networking or related issues - all new incoming data will be discarded, pipes to stdout, and stderr 
are still will be alive/valid. Also as ``bftee`` has it's own buffer it consumes stdin in async  
To compile ``bftee``:
```shell script
# CentOS:
yum install -y gcc
# Ubuntu:
apt install build-essential
# Compile
gcc "bftee.c" -o bftee
mv bftee /usr/bin
```
Now just use an example of implementation from ``client.sh`` 

