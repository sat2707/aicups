from core import settings
from core.utils import sign


class Passenger(object):
    PASSENGER_STATE = {
        'waiting_for_elevator': 1,
        'moving_to_elevator': 2,
        'returning': 3,
        'moving_to_floor': 4,
        'using_elevator': 5,
        'exiting': 6,
        'away': 7,
        'walking_on_floor': 8,
        'for_delete': 9,
    }

    def __init__(self, id, x, y, floors_queue, weight, type):
        self.id = id
        self.x = x
        self.y = y
        self.floor = y
        self.from_floor = y
        self.floors_queue = list(floors_queue)
        self.weight = weight
        self.type = type

        self.base_x = x

        self.reward = settings.PASSENGERS['REWARD']
        self.speed = settings.PASSENGERS['SPEED']['HORIZONTAL']
        self.enemy_reward = settings.PASSENGERS['ENEMY_REWARD']
        self.walking_time = settings.PASSENGERS['WALKING_TIME']
        self.time_to_away = settings.PASSENGERS['TIME_TO_AWAY']
        self.move_to_floor = settings.PASSENGERS['MOVE_TO_FLOOR']

        self.elevator = None
        self.reward_ready = False
        self.dest_floor = self.floors_queue.pop(0)
        self.state = self.PASSENGER_STATE['waiting_for_elevator']
        self.time_to_floor = 0

    def get_base_x(self):
        if self.type == settings.PLAYERS['FIRST_PLAYER_KEY']:
            return -settings.BUILDING['PASSENGER_SPAWN_POSITION']
        return settings.BUILDING['PASSENGER_SPAWN_POSITION']

    def get_type(self):
        return self.type

    def get_elevator_type(self):
        return self.elevator.get_type()

    def move_in_elevator(self):
        if self.is_using_elevator():
            self.y = self.elevator.y

    def is_waiting_for_elevator(self):
        return self.state == self.PASSENGER_STATE['waiting_for_elevator']

    def is_returning(self):
        return self.state == self.PASSENGER_STATE['returning']

    def is_walking_on_floor(self):
        return self.state == self.PASSENGER_STATE['walking_on_floor']

    def is_reward_ready(self):
        return self.reward_ready

    def is_using_elevator(self):
        return self.state == self.PASSENGER_STATE['using_elevator']

    def is_for_delete(self):
        return self.state == self.PASSENGER_STATE['for_delete']

    def get_player_to_score(self):
        if self.elevator:
            return self.elevator.type

    def serialize(self):
        return {
            "state": self.state,
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "time_to_away": self.time_to_away,
            "weight": self.weight,
            "type": self.type,
            "dest_floor": self.dest_floor,
            "from_floor": self.from_floor,
            "floor": self.floor,
            "elevator": self.elevator.id if self.elevator else None
        }

    def get_visio(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "state": self.state,
            "id": self.id,
            "time_to_away": self.time_to_away,
        }

    def delete(self):
        self.state = self.PASSENGER_STATE['for_delete']

    def may_go_to_ladder(self):
        if self.state in (
            self.PASSENGER_STATE['waiting_for_elevator'],
            self.PASSENGER_STATE['moving_to_elevator'],
            self.PASSENGER_STATE['returning'],
        ):
            return True
        else:
            return False

    def go_to_ladder(self):
        self.time_to_away = settings.PASSENGERS['TIME_TO_AWAY']
        if self.type == settings.PLAYERS["FIRST_PLAYER_KEY"]:
            self.x = -settings.BUILDING['LADDER_POSITION']
        else:
            self.x = settings.BUILDING['LADDER_POSITION']
        self.state = self.PASSENGER_STATE['moving_to_floor']

        if self.y < self.dest_floor:
            self.time_to_floor = abs(self.from_floor - self.dest_floor) * settings.PASSENGERS["SPEED"]["UP"]
        else:
            self.time_to_floor = abs(self.from_floor - self.dest_floor) * settings.PASSENGERS["SPEED"]["DOWN"]

        if self.elevator:
            if self in self.elevator.passengers:
                self.elevator.passengers.remove(self)
            self.elevator = None

    def arrived_to_floor(self, dest_floor):
        if len(self.floors_queue) == 0:
            self.state = self.PASSENGER_STATE['for_delete']
            return
        self.y = dest_floor
        self.floor = dest_floor
        self.from_floor = self.floor
        self.dest_floor = self.floors_queue.pop(0)
        self.state = self.PASSENGER_STATE['walking_on_floor']
        self.reward_ready = False

    def on_tick(self):
        if self.time_to_away == 0 and self.may_go_to_ladder():
            self.go_to_ladder()
            return

        if self.may_go_to_ladder():
            self.time_to_away -= 1

        if self.state == self.PASSENGER_STATE['waiting_for_elevator']:
            if self.elevator:
                self.state = self.PASSENGER_STATE['moving_to_elevator']
            return

        if self.state == self.PASSENGER_STATE['moving_to_elevator']:
            if self.elevator.floor == self.floor and self.elevator.is_filling():
                if abs(self.x - self.elevator.x) >= self.speed:
                    self.move(x=sign(self.elevator.x - self.x))
                elif self.elevator.floor == self.from_floor and self.elevator.can_enter():
                    self.elevator.enter(self)
                    self.state = self.PASSENGER_STATE['using_elevator']
                else:
                    self.elevator = None
                    self.state = self.PASSENGER_STATE['returning']
            else:
                self.elevator = None
                self.state = self.PASSENGER_STATE['returning']
            return

        if self.state == self.PASSENGER_STATE['moving_to_floor']:
            dest_floor = self.dest_floor
            if self.y < dest_floor:
                self.move(y=1. / settings.PASSENGERS["SPEED"]["UP"])
            elif self.y > dest_floor:
                self.move(y=-1. / settings.PASSENGERS["SPEED"]["DOWN"])
            self.time_to_floor -= 1

            if self.time_to_floor == 0:
                self.arrived_to_floor(dest_floor)
            return

        if self.state == self.PASSENGER_STATE['returning']:
            if self.elevator:
                self.state = self.PASSENGER_STATE['moving_to_elevator']
            base_x = self.get_base_x()
            if abs(base_x - self.x) > self.speed:
                self.move(x=-sign(self.x - base_x))
            else:
                self.x = base_x
                self.state = self.PASSENGER_STATE['waiting_for_elevator']
            return

        if self.state == self.PASSENGER_STATE['using_elevator']:
            return

        if self.state == self.PASSENGER_STATE['exiting']:
            self.move_to_floor -= 1
            if self.move_to_floor == 0:
                self.move_to_floor = settings.PASSENGERS['MOVE_TO_FLOOR']
                if self.floor == 0 or len(self.floors_queue) == 0:
                    self.state = self.PASSENGER_STATE['for_delete']
                    return
                self.state = self.PASSENGER_STATE['walking_on_floor']
                self.from_floor = self.floor
                self.dest_floor = self.floors_queue.pop(0)
                return

            self.move(x=sign(self.x))
            return

        if self.state == self.PASSENGER_STATE['walking_on_floor']:
            if self.walking_time == 0:
                self.walking_time = settings.PASSENGERS['WALKING_TIME']
                self.state = self.PASSENGER_STATE['waiting_for_elevator']
                self.time_to_away = settings.PASSENGERS['TIME_TO_AWAY']
                self.x = self.get_base_x()
                self.elevator = None
                return
            self.walking_time -= 1
            return

    def determine_score(self):
        self.reward_ready = False
        diff = abs(self.dest_floor - self.from_floor)
        if self.floor != self.dest_floor:
            return 0
        if self.elevator.get_type() == self.type:
            return diff * self.reward
        else:
            return diff * self.reward * self.enemy_reward

    def exit(self, floor):
        self.reward_ready = True
        self.state = self.PASSENGER_STATE['exiting']
        self.floor = floor
        self.y = floor

    def move(self, **kwargs):
        self.x += kwargs.get('x', 0) * self.speed
        self.y += kwargs.get('y', 0)
