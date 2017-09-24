from itertools import chain


class Elevator(object):
    def __init__(self, id, y, passengers, state, speed, floor, next_floor, time_on_floor, type):
        self.id = id
        self.y = y
        self.passengers = [Passenger(**p) for p in passengers]
        self.state = state
        self.speed = speed
        self.time_on_floor = time_on_floor
        self.next_floor = next_floor
        self.messages = []
        self.type = type
        self.floor = floor

    def go_to_floor(self, floor):
        # todo: deny to enemy lift here (on server denied)
        try:
            self.next_floor = int(floor)
            self.messages.append({
                "command": "go_to_floor",
                "args": {
                    "elevator_id": self.id,
                    "floor": floor
                }
            })
        except (ValueError, TypeError):
            return


class Passenger(object):
    def __init__(self, id, elevator, x, y, state, time_to_away, from_floor, dest_floor, type, floor, weight):
        self.id = id
        self.elevator = elevator
        self.from_floor = from_floor
        self.dest_floor = dest_floor
        self.time_to_away = time_to_away
        self.state = state
        self.messages = []
        self.x = x
        self.y = y
        self.type = type
        self.floor = floor
        self.weight = weight

    def set_elevator(self, elevator):
        self.elevator = elevator
        self.messages.append({
            'command': 'set_elevator_to_passenger',
            'args': {
                'passenger_id': self.id,
                'elevator_id': elevator.id
            }
        })

    def has_elevator(self):
        return self.elevator is not None


class Debug(object):
    def __init__(self):
        self._messages = []

    @property
    def messages(self):
        pass

    @messages.getter
    def messages(self):
        messages = self._messages
        self._messages = []
        return messages

    def log(self, text):
        self._messages.append({
            'command': 'log',
            'args': {
                'text': str(text)
            }
        })

    def exception(self, text):
        self._messages.append({
            'command': 'exception',
            'args': {
                'text': str(text)
            }
        })


class API(object):
    def __init__(self, type):
        self.debug = Debug()
        self.strategy = None
        self.color = type
        try:
            from strategy import Strategy
            self.strategy = Strategy(self.debug, self.color)
        except Exception as e:
            self.debug.exception(str(e))

    @staticmethod
    def parse_state(state):
        my_passengers = state['my_passengers']
        enemy_passengers = state['enemy_passengers']
        my_elevators = state['my_elevators']
        enemy_elevators = state['enemy_elevators']
        my_elevators = [Elevator(**e) for e in my_elevators]
        enemy_elevators = [Elevator(**e) for e in enemy_elevators]
        my_passengers = [Passenger(**p) for p in my_passengers]
        enemy_passengers = [Passenger(**p) for p in enemy_passengers]
        return my_elevators, my_passengers, enemy_elevators, enemy_passengers

    def turn(self, state):
        my_elevators, my_passengers, enemy_elevators, enemy_passengers = self.parse_state(state)
        try:
            if self.strategy:
                self.strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)
        except Exception as e:
            self.debug.exception(repr(e))

        result = list(chain(*[obj.messages for obj in my_elevators + my_passengers + enemy_passengers + [self.debug]]))
        return result
