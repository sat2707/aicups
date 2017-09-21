# (Лифт) атрибуты только для чтения
class Elevator:
    def __init__(self, add_action, id: int, y: int, passengers: list, state: int, speed: float,
                 floor: int, next_floor: int, time_on_floor: int, type: str):
        self.add_action = add_action
        self.id = id
        self.y = y
        self.passengers = [Passenger(add_action, **p) for p in passengers]
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
            self.add_action('go_to_floor', {"elevator_id": self.id, "floor": floor})
        except (ValueError, TypeError):
            return

# (Пассажир) атрибуты только для чтения
class Passenger:
    def __init__(self, add_action, id: int, elevator, x: float, y: float, state: int, time_to_away: int, from_floor: int, dest_floor: int, type: str, floor: float, weight: float):
        self.add_action = add_action
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

    # проверить, назначен ли лифт
    def has_elevator(self):
        return self.elevator is not None

    def set_elevator(self, elevator: Elevator):
        self.elevator = elevator
        self.add_action('set_elevator_to_passenger', {'passenger_id': self.id, 'elevator_id': elevator.id})


class Debug:
    def __init__(self, add_action):
        self.add_action = add_action

    def exception(self, text: Exception):
        self.add_action('exception', {'text': str(text)})

    def log(self, text):
        self.add_action('log', {'text': str(text)})


class API:
    def __init__(self):
        try:
            from core.strategy import Strategy
            self.strategy = Strategy()
        except Exception as e:
            self.strategy = None
            self.instance_exception = e

    def generate_actions(self, state):
        actions = []
        add_action = lambda action, args: actions.append({'command': action, 'args': args})
        dummy_action = lambda action, args: action

        my_passengers = state['my_passengers']
        enemy_passengers = state['enemy_passengers']
        my_elevators = state['my_elevators']
        enemy_elevators = state['enemy_elevators']
        my_elevators = [Elevator(add_action, **e) for e in my_elevators]
        enemy_elevators = [Elevator(dummy_action, **e) for e in enemy_elevators]
        my_passengers = [Passenger(add_action, **p) for p in my_passengers]
        enemy_passengers = [Passenger(add_action, **p) for p in enemy_passengers]

        debug = Debug(add_action)
        try:
            if self.strategy:
                self.strategy.set_debug(debug)
                self.strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)
            else:
                if self.instance_exception:
                    debug.exception(self.instance_exception)
                    self.instance_exception = None
        except Exception as e:
            debug.exception(e)
        return actions
