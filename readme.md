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

## Client side

See example of implementation from `client.sh`

