import os
import socket
import json
from asyncio import get_event_loop, open_connection
from core.api import API


class Client:
    def __init__(self, loop, solution_id):
        self.solution_id = solution_id
        self.api = API()
        self.loop = loop
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.setblocking(False)

    async def ask_for_grant(self, reader, writer):
        await self.send_to_server({
            'solution_id': self.solution_id
        }, writer)

        data = await reader.readuntil(b'\n')
        data = json.loads(data.decode())
        grant = data.get('message') == 'beginning'
        return grant, reader

    async def send_to_server(self, message, writer):
        message = json.dumps(message).encode('unicode_escape') + b'\n'
        writer.write(message)
        return await writer.drain()

    async def start(self, host, port):
        reader, writer = await open_connection(host, port)
        grant, reader = await self.ask_for_grant(reader, writer)
        while grant:
            data = await reader.readuntil(b'\n')
            data = json.loads(data.decode())

            if data.get('message') == 'down':
                break

            actions = self.api.generate_actions(data)
            await self.send_to_server(actions, writer)


world_host = os.environ.get('WORLD_NAME', '127.0.0.1')
world_port = 8000
solution_id = os.environ.get('SOLUTION_ID', 1)

loop = get_event_loop()
client = Client(loop, solution_id)
future = client.start(world_host, world_port)
loop.run_until_complete(future)
