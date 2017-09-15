import json
import os
from random import randint

import tornado
import tornado.gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient

from core.api import API

host = os.environ.get('WORLD_NAME', '127.0.0.1')
port = 8000


class Client(object):
    def __init__(self, solution_id):
        self.solution_id = solution_id
        self.color = None

    @staticmethod
    def dump_message(message):
        message = '{}\n'.format(json.dumps(message).encode('string-escape'))
        return message

    @tornado.gen.coroutine
    def connect(self, host, port):
        self.stream = yield TCPClient().connect(host, port)
        self.stream.set_close_callback(self.on_close)
        self.send_message({'solution_id': self.solution_id})
        try:
            data = yield self.stream.read_until('\n')
            data = json.loads(data)
            if data['message'] == 'beginning':
                self.strategy_loop(data['color'])
            else:
                IOLoop.instance().stop()
        except StreamClosedError:
            IOLoop.instance().stop()

    @tornado.gen.coroutine
    def send_message(self, msg):
        msg = self.dump_message(msg)
        self.stream.write(msg)

    @tornado.gen.coroutine
    def strategy_loop(self, color):
        api = API(color)
        while True:
            try:
                data = yield self.stream.read_until('\n')
                data = json.loads(data)
                if data.get('message') == 'down':
                    break
                turn = api.turn(data)
                yield self.stream.write(self.dump_message(turn))
            except StreamClosedError:
                IOLoop.instance().stop()

    @staticmethod
    def on_close():
        IOLoop.instance().stop()


solution_id = os.environ.get('SOLUTION_ID', randint(0, 1000))
c = Client(solution_id).connect(host, port)
IOLoop.instance().start()
