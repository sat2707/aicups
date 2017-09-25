from core import settings

class Elevator(object):
    ELEVATOR_STATE = {
        'waiting': 0,
        'moving': 1,
        'opening': 2,
        'filling': 3,
        'closing': 4
    }

    def __init__(self, id, x, y, floor, type):
        self.id = id
        self.x = x
        self.y = y
        self.floor = floor
        self.type = type

        self.speed = 1./settings.ELEVATORS['TICKS_PER_FLOOR']
        self.opening_ticks = settings.ELEVATORS['OPENING_TICKS']
        self.closing_ticks = settings.ELEVATORS['CLOSING_TICKS']
        self.soft_capacity = settings.ELEVATORS['SOFT_CAPACITY']
        self.filling_delay = settings.ELEVATORS['FILLING_DELAY']
        self.critical_capacity = settings.ELEVATORS['CRITICAL_CAPACITY']
        self.time_on_the_floor_to_load_enemy_passenger = settings.ELEVATORS['TIME_ON_THE_FLOOR_TO_LOAD_ENEMY_PASSENGER']

        self.time_to_floor = 0
        self.next_floor = -1
        self.passengers = []
        self.time_on_the_floor = 0
        self.time_on_the_floor_with_opened_doors = 0
        self.current_filling_delay = settings.ELEVATORS['FILLING_DELAY']
        self.state = self.ELEVATOR_STATE['filling']

    def on_tick(self):
        if self.state != self.ELEVATOR_STATE['moving']:
            self.time_on_the_floor += 1

        if self.state == self.ELEVATOR_STATE['filling']:
            self.time_on_the_floor_with_opened_doors += 1
        else:
            self.time_on_the_floor_with_opened_doors = 0

        if self.next_floor != -1 and self.state == self.ELEVATOR_STATE['waiting']:
            if self.floor != self.next_floor:
                self.state = self.ELEVATOR_STATE['moving']

                if self.y > self.next_floor:
                    self.time_to_floor = abs(self.floor - self.next_floor) / self.get_speed(with_weight=False)
                elif self.y < self.next_floor:
                    self.time_to_floor = abs(self.floor - self.next_floor) / self.get_speed()

            else:
                self.state = self.ELEVATOR_STATE['opening']
            return

        if self.state == self.ELEVATOR_STATE['moving']:
            self.time_on_the_floor = 0
            self.moving()
            return

        if self.state == self.ELEVATOR_STATE['opening']:
            self.opening_ticks -= 1
            if self.opening_ticks == 0:
                self.next_floor = -1
                self.state = self.ELEVATOR_STATE['filling']
                self.opening_ticks = settings.ELEVATORS['OPENING_TICKS']
                return
            return

        if self.state == self.ELEVATOR_STATE['filling']:
            self.current_filling_delay -= 1
            if self.current_filling_delay <= 0:
                can_close = True
            else:
                can_close = False

            for p in list(self.passengers):
                if self.floor == p.dest_floor:
                    self.passengers.remove(p)
                    p.exit(self.floor)
                can_close = can_close and p.is_using_elevator()

            if self.next_floor != -1 and can_close and self.next_floor != self.floor:
                self.current_filling_delay = settings.ELEVATORS['FILLING_DELAY']
                self.state = self.ELEVATOR_STATE['closing']
            return

        if self.state == self.ELEVATOR_STATE['closing']:
            self.closing_ticks -= 1
            if self.closing_ticks == 0:
                self.state = self.ELEVATOR_STATE['waiting']
                self.closing_ticks = settings.ELEVATORS['CLOSING_TICKS']
                return
            return

    def is_full(self):
        return len(self.passengers) == self.critical_capacity

    def get_type(self):
        return self.type

    def get_speed(self, with_weight=True):
        if with_weight:
            multiple = reduce(lambda x, y: x * y, map(lambda x: x.weight, self.passengers), 1)
            if len(self.passengers) > self.soft_capacity:
                multiple *= settings.ELEVATORS['OVERLOAD_MULTIPLY']

            return self.speed / multiple
        else:
            return self.speed

    def can_enter(self):
        return self.state == self.ELEVATOR_STATE['filling'] and len(self.passengers) < self.critical_capacity

    def enter(self, passenger):
        if passenger not in self.passengers:
            self.passengers.append(passenger)

    def serialize(self):
        return {
            "id": self.id,
            "state": self.state,
            "floor": self.floor,
            "passengers": [p.serialize() for p in self.passengers],
            "type": self.type,
            "y": self.y,
            "speed": self.get_speed(),
            "next_floor": self.next_floor,
            "time_on_floor": self.time_on_the_floor
        }

    def get_visio(self):
        return {
            "x": self.x,
            "y": self.y,
            "state": self.state,
            "type": self.type
        }

    def get_elevator_type(self):
        return self.type

    def ready_for_enemy_passenger(self):
        if self.time_on_the_floor_with_opened_doors >= self.time_on_the_floor_to_load_enemy_passenger:
            return True
        return False

    def current_floor(self):
        return self.floor

    def go_to_floor(self, floor):
        if 0 < floor <= settings.BUILDING['FLOORS_COUNT'] and not self.is_moving():
            self.next_floor = floor

    def moving(self):
        self.time_to_floor -= 1
        dest_floor = self.next_floor
        if self.time_to_floor <= 0:
            self.floor = dest_floor
            self.y = dest_floor

            self.state = self.ELEVATOR_STATE['opening']
            return

        if self.y > dest_floor:
            self.move_down()
        elif self.y < dest_floor:
            self.move_up()

    def move_down(self):
        next_floor_y = self.floor + 1
        if abs(next_floor_y - self.y) < self.get_speed(with_weight=False):
            self.floor -= 1

        self.move(y=-1, with_weight=False)

        for p in self.passengers:
            p.move_in_elevator()

    def move_up(self):
        next_floor_y = self.floor - 1
        elev_y = self.y

        if abs(elev_y - next_floor_y) < self.get_speed():
            self.floor += 1

        self.move(y=1)
        for p in self.passengers:
            p.move_in_elevator()

    def move(self, with_weight=True, **kwargs):
        self.y += kwargs.get('y', 0) * self.get_speed(with_weight=with_weight)

    def is_moving(self):
        return self.state == self.ELEVATOR_STATE['moving']

    def is_filling(self):
        return self.state == self.ELEVATOR_STATE['filling']
