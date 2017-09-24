# coding=utf-8
import json
import os

from datetime import datetime, timedelta
import requests
from cStringIO import StringIO

from tornado.iostream import StreamClosedError

from core import settings
from core.api import API
from tornado.tcpserver import TCPServer
import tornado.gen
import tornado.ioloop
import tornado.gen
import gzip


class Client(object):
    max_client_time = int(os.environ.get('MAX_CLIENT_TIME', 120))

    def __init__(self, stream):
        self.solution_id = None
        self.stream = stream
        self.total_time = 0
        self.is_close = False

    def set_solution_id(self, solution_id):
        self.solution_id = solution_id

    def send(self, message):
        self.stream.write(self.dump_message(message))

    def close(self):
        self.is_close = True
        self.stream.close()

    @staticmethod
    def dump_message(message):
        message = '{}\n'.format(json.dumps(message, separators=(',', ':')).encode('string-escape'))
        return message

    @tornado.gen.coroutine
    def read_messages(self):
        message = []
        try:
            before_read_time = datetime.now()
            message = yield tornado.gen.with_timeout(timedelta(seconds=10), self.stream.read_until('\n'))
            tick_time = datetime.now() - before_read_time
            message = message.strip()
            try:
                message = json.loads(message, strict=False)
            except ValueError as e:
                message = [{
                        'command': 'fatal_error',
                        'args': {
                            'text': u'Ошибка парсинга ответов'
                        }
                    }]
                raise ValueError(e)
            self.total_time += tick_time.total_seconds()
        except tornado.gen.TimeoutError:
            self.is_close = True
            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Время выполнения одного тика превышено'
                }
            })
        except StreamClosedError:
            self.is_close = True
            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Стратегия аварийно завершила работу'
                }
            })

        if self.total_time > self.max_client_time:
            self.close()

            message.append({
                'command': 'fatal_error',
                'args': {
                    'text': u'Время выполнения стратегии первышено'
                }
            })
        raise tornado.gen.Return(message)


class WorldHandler(object):
    api = API()
    red_client = None
    blue_client = None
    ticks_count = int(os.environ.get('TICKS_COUNT', 7200))
    result = []

    client_player = {}

    @tornado.gen.coroutine
    def connect(self, stream, address):
        current_client = Client(stream)
        try:
            messages = yield current_client.read_messages()
            solution_id = int(messages.get('solution_id'))
        except (ValueError, TypeError):
            solution_id = None
        except StreamClosedError:
            solution_id = None
        current_client.set_solution_id(solution_id)

        if self.red_client is None:
            self.red_client = current_client
        elif self.blue_client is None:
            self.blue_client = current_client
            self.start()
        else:
            pass

    def shutdown(self):
        if not self.blue_client.is_close:
            self.blue_client.send({'message': 'down'})
            self.blue_client.close()

        if not self.red_client.is_close:
            self.red_client.send({'message': 'down'})
            self.red_client.close()

        tornado.ioloop.IOLoop.instance().stop()

    @staticmethod
    def write_result(data):
        f = open('{}/../visualizer/game.js'.format(os.path.dirname(os.path.realpath(__file__))), 'w')
        f.write("var data = ")
        f.write(json.dumps(data))
        f.write(";")
        f.close()

    @tornado.gen.coroutine
    def start(self):
        self.api.create_players(self.red_client, self.blue_client)
        self.red_client.send({'message': 'beginning', 'color': 'FIRST_PLAYER'})
        self.blue_client.send({'message': 'beginning', 'color': 'SECOND_PLAYER'})

        for _ in range(0, self.ticks_count):
            blue_message = []
            if not self.blue_client.is_close:
                self.blue_client.send(self.api.get_world_state_for(self.blue_client))
                blue_message = yield self.blue_client.read_messages()

            red_message = []
            if not self.red_client.is_close:
                self.red_client.send(self.api.get_world_state_for(self.red_client))
                red_message = yield self.red_client.read_messages()

            self.api.apply_commands(blue_message, self.blue_client)
            self.api.apply_commands(red_message, self.red_client)
            self.api.tick()
            self.result.append(self.api.get_visio_state())

        try:
            self.write_result({
                'config': settings.BUILDING_VISIO,
                'game_data': self.result,
                'players': {
                    "FIRST_PLAYER": self.red_client.solution_id,
                    "SECOND_PLAYER": self.blue_client.solution_id,
                }
            })
        except Exception as e:
            print e

        self.shutdown()


class Server(TCPServer):
    def __init__(self):
        self.world_handler = WorldHandler()
        super(Server, self).__init__()

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        self.world_handler.connect(stream, address)


server = Server().listen(8000)
tornado.ioloop.IOLoop.instance().start()
