from core import settings
from core.world import World


class API(object):
    def __init__(self):
        self.world = World()
        self.exception_text = []
        self.log_text = []
        self.client_player = {}
        self.red_client = None
        self.blue_client = None
        self.player_debug = {}

    def get_world_state_for(self, client):
        return self.world.get_state_for(self.client_player[client])

    def create_players(self, red_client, blue_client):
        self.red_client = red_client
        self.blue_client = blue_client
        self.client_player = {
            red_client: settings.PLAYERS['FIRST_PLAYER_KEY'],
            blue_client: settings.PLAYERS['SECOND_PLAYER_KEY']
        }
        self.player_debug = {
            settings.PLAYERS['FIRST_PLAYER_KEY']: {
                'exceptions': [],
                'logs': [],
                'fatal_error': [],
            },
            settings.PLAYERS['SECOND_PLAYER_KEY']: {
                'exceptions': [],
                'logs': [],
                'fatal_error': [],
            }
        }

    def clear_client_debug(self):
        self.player_debug = {k: {'exceptions': [], 'logs': [], 'fatal_error': []} for k, _ in self.player_debug.iteritems()}

    def apply_commands(self, commands, client):
        player = self.client_player.get(client)
        for command in commands:
            command_name = command.get("command")
            args = command.get("args")
            if command_name:
                method_to_call = getattr(self, command_name, None)
                if method_to_call is None:
                    continue
                try:
                    method_to_call(player=player, **args)
                except TypeError:
                    pass

    def tick(self):
        self.world.tick()

    def get_visio_state(self):
        world_state = self.world.get_visio_state()
        world_state.update({'debug': {k: v for k, v in self.player_debug.iteritems()}})
        self.clear_client_debug()
        return world_state

    def get_state(self):
        return self.world.get_state()

    def go_to_floor(self, player, floor, elevator_id):
        elevator = filter(lambda x: x.id == elevator_id, self.world.get_elevator_for(player))
        if not elevator:
            return
        elevator = elevator[0]
        if isinstance(floor, int):
            elevator.go_to_floor(floor)

    def set_elevator_to_passenger(self, player, passenger_id, elevator_id):
        elevator = filter(lambda x: x.id == elevator_id, self.world.get_elevator_for(player))
        passenger = filter(lambda x: x.id == passenger_id, self.world.get_passengers())
        if not passenger:
            return
        passenger = passenger[0]

        if not elevator:
            return
        elevator = elevator[0]
        self.world.building.set_passenger_elevator(passenger, elevator)

    def exception(self, player, text):
        if len(self.player_debug[player]['exceptions']) < 10000:
            self.player_debug[player]['exceptions'].append(text[:100])

    def log(self, player, text):
        if len(self.player_debug[player]['logs']) < 10000:
            self.player_debug[player]['logs'].append(text[:100])

    def fatal_error(self, player, text):
        if len(self.player_debug[player]['fatal_error']) < 10000:
            self.player_debug[player]['fatal_error'].append(text[:100])
