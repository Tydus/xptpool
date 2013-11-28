#!/usr/bin/python

import tornado.ioloop
import tornado.tcpserver
import tornado.httpclient
import functools

import packethandler

class BaseConnection(object):
    clients = Set()
    def __init__(self, stream, addr):
        print "New connection from %s" % self._addr
        self._stream = stream
        self._addr = addr
        self._stream.set_close_callback(self.on_close)
        clients.add(self)
        self.handle_read()

    @classmethod
    def broadcast(self, data):
        for i in self.clients:
            i.write(data)

    def on_close(self):
        clients.remove(self)


class xptConnection(BaseConnection):
    def read(self):
        self._stream.read_bytes(4, self.on_header)

    def on_header(self, header):
        type, len = struct.unpack("<BL", header + '\0')
        self._stream.read_bytes(len, functools.partial(
            self.on_data, type
        ))

    def on_data(self, type, data):
        packethandler.packetHandler.get(type, 0).read(StringIO(data))

    def write(self, type, data):
        self._stream.write(struct.pack("<BL", type, len(data))[:4])
        self._stream.write(data)


class xptServer(tornado.tcpserver.TCPServer):
    def handle_stream(self, stream, addr):
        xptConnection(stream, addr)

if __name__ == '__main__':    
    print "Server start ......"
    xptServer().listen(10034)
    tornado.ioloop.IOLoop.instance().start()
