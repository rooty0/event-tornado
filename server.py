import os
from datetime import datetime
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
from tornado.iostream import PipeIOStream


class SafeFileIOStream:
    def __init__(self, fname):
        self.fname = fname

        files_dir = os.path.dirname(fname)
        if not os.path.exists(files_dir):
            os.mkdir(files_dir)

    def __enter__(self):
        # Create file
        os.open(self.fname, os.O_CREAT)
        # Create stream
        fd = os.open(self.fname, os.O_WRONLY)
        self.stream = PipeIOStream(fd)
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close stream
        self.stream.close()


class EventServer(TCPServer):
    async def handle_stream(self, stream, address):

        log_file = "events/{}".format(datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f.log'))

        print("New client is connected {}:{}. Redirecting output to {}".format(
            address[0],
            address[1],
            log_file
        ))

        with SafeFileIOStream(log_file) as stream_log:
            while True:
                try:
                    await stream_log.write(await stream.read_bytes(1))
                except StreamClosedError:
                    await stream_log.write(b"------------------END------------------\n")
                    print("Bye-bye {}:{}".format(address[0], address[1]))
                    break


if __name__ == '__main__':
    # TODO: SSL support https://www.tornadoweb.org/en/stable/tcpserver.html
    server = EventServer()
    server.bind(8888)
    server.start(0)  # Forks multiple sub-processes

    ioloop = IOLoop.current()

    try:
        ioloop.start()
    except KeyboardInterrupt:
        ioloop.stop()
