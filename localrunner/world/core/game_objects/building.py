from random import sample, randint

from core import settings
from core.game_objects.elevator import Elevator
from core.game_objects.passenger import Passenger
from core.utils import group_size_generator


class Building(object):
    def __init__(self):
        self.floors_count = settings.BUILDING['FLOORS_COUNT']
        self.players_score = {
            settings.PLAYERS['FIRST_PLAYER_KEY']: 0,
            settings.PLAYERS['SECOND_PLAYER_KEY']: 0
        }

        first_player_elevators = []
        second_player_elevators = []
        elevator_id = 1
        for i in range(settings.BUILDING['ELEVATORS_FOR_PASSENGER_COUNT']):
            elevator_x = settings.BUILDING['FIRST_ELEVATOR_POSITION'] + i * (settings.BUILDING['ELEVATOR_IN_GROUP_OFFSET'])
            elevator_y = settings.BUILDING['FIRST_FLOOR']
            first_player_elevators.append(Elevator(elevator_id, -elevator_x, elevator_y, settings.BUILDING['FIRST_FLOOR'], settings.PLAYERS['FIRST_PLAYER_KEY']))
            elevator_id += 1
            second_player_elevators.append(Elevator(elevator_id, elevator_x, elevator_y, settings.BUILDING['FIRST_FLOOR'], settings.PLAYERS['SECOND_PLAYER_KEY']))
            elevator_id += 1

        self.players_elevators = {
            settings.PLAYERS['FIRST_PLAYER_KEY']: first_player_elevators,
            settings.PLAYERS['SECOND_PLAYER_KEY']: second_player_elevators,
        }

        self.all_passengers = []
        self.passenger_id = 1

    def get_score_for(self, player):
        return self.players_score[player]

    def get_player_elevator(self, player):
        return self.players_elevators.get(player)

    def set_passenger_elevator(self, passenger, elevator):
        if (passenger.is_waiting_for_elevator() or passenger.is_returning()) and elevator.current_floor() == passenger.from_floor and elevator.is_filling() and not elevator.is_full():
            if elevator.get_type() != passenger.get_type() and not elevator.ready_for_enemy_passenger():
                return

            if passenger.elevator:
                passenger_elevator_distance = abs(passenger.x - passenger.elevator.x)
                passenger_new_elevator_distance = abs(passenger.x - elevator.x)
                if passenger_new_elevator_distance < passenger_elevator_distance:
                    passenger.elevator = elevator
                return

            if elevator.get_type() == passenger.get_type():
                passenger.elevator = elevator
                return

            if elevator.ready_for_enemy_passenger():
                passenger.elevator = elevator
                return

    def spawn(self):
        floors_queue = sample(range(2, settings.BUILDING['FLOORS_COUNT'] + 1),
                              settings.BUILDING['FLOORS_QUEUE_LEN']()) + [settings.BUILDING["FIRST_FLOOR"]]
        weight = settings.PASSENGERS['WEIGHT']()

        passenger_x = settings.BUILDING['PASSENGER_SPAWN_POSITION']
        passenger_y = settings.BUILDING['FIRST_FLOOR']

        first_passenger = Passenger(self.passenger_id, -passenger_x, passenger_y, floors_queue, weight, settings.PLAYERS['FIRST_PLAYER_KEY'])
        self.all_passengers.append(first_passenger)
        self.passenger_id += 1

        second_passenger = Passenger(self.passenger_id, passenger_x, passenger_y, floors_queue, weight, settings.PLAYERS['SECOND_PLAYER_KEY'])
        self.all_passengers.append(second_passenger)
        self.passenger_id += 1

    def on_tick(self):
        for e in self.players_elevators[settings.PLAYERS['FIRST_PLAYER_KEY']] + self.players_elevators[settings.PLAYERS['SECOND_PLAYER_KEY']]:
            e.on_tick()
        for p in list(self.all_passengers):
            p.on_tick()
            if p.is_reward_ready():
                self.players_score[p.get_elevator_type()] += p.determine_score()
                p.type = p.elevator.type
            if p.is_for_delete():
                self.all_passengers.remove(p)
