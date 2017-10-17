#! /usr/bin/env python
#coding=utf-8

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
import struct
from tornado import gen

class TcpConnection(object):
    def __init__(self,stream,address):
        self._stream=stream
        self._address=address
        self._stream.set_close_callback(self.on_close)

    @gen.coroutine
    def send_messages(self):
        yield self.send_message(b'hello \n')
        response1 = yield self.read_message()
        print(response1)
        yield self.send_message(b'world \n')
        # You can receive the result in-line, but you need to wrap with ( ):
        print((yield self.read_message()))

    def read_message(self):
        return self._stream.read_until(b'\n')

    def send_message(self,data):
        return self._stream.write(data)

    def on_close(self):
        print("the monitored %d has left",self._address)

class MonitorServer(TCPServer):
    @gen.coroutine
    def handle_stream(self,stream,address):
        print("new connection",address,stream)
        conn = TcpConnection(stream,address)
        yield conn.send_messages()


if  __name__=='__main__':
    print('server start .....')
    server=MonitorServer()
    server.listen(20000)
    IOLoop.instance().start()

