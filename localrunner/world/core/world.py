from itertools import groupby

from core import settings
from core.game_objects.building import Building


class World(object):
    def __init__(self):
        self.building = Building()
        self.counter = 0
        self.next_spawn = settings.BUILDING['TICK_TO_SPAWN']
        self.building.spawn()

    def tick(self):
        self.counter += 1
        self.building.on_tick()
        if self.counter < settings.BUILDING['TICK_COUNT_TO_SPAWN'] and self.counter % self.next_spawn == 0:
            self.next_spawn = settings.BUILDING['TICK_TO_SPAWN']
            self.building.spawn()

    def get_elevator_for(self, player):
        return self.building.players_elevators[player]

    def get_state_for(self, player):
        if player == settings.PLAYERS['FIRST_PLAYER_KEY']:
            return {
                "my_elevators": [e.serialize() for e in self.get_red_elevators()],
                "enemy_elevators": [e.serialize() for e in self.get_blue_elevators()],
                "my_passengers": [p.serialize() for p in self.get_red_passengers() if not p.is_walking_on_floor()],
                "enemy_passengers": [p.serialize() for p in self.get_blue_passengers() if not p.is_walking_on_floor()],
            }
        return {
            "my_elevators": [e.serialize() for e in self.get_blue_elevators()],
            "enemy_elevators": [e.serialize() for e in self.get_red_elevators()],
            "my_passengers": [p.serialize() for p in self.get_blue_passengers() if not p.is_walking_on_floor()],
            "enemy_passengers": [p.serialize() for p in self.get_red_passengers() if not p.is_walking_on_floor()],
        }

    def get_visio_state(self):
        red = settings.PLAYERS["FIRST_PLAYER_KEY"]
        blue = settings.PLAYERS["SECOND_PLAYER_KEY"]
        return {
            "elevators": [e.get_visio() for e in list(reversed(self.get_red_elevators())) + self.get_blue_elevators()],
            "passengers": [p.get_visio() for p in self.get_passengers() if not p.is_walking_on_floor()],
            "scores": {
                red: self.building.get_score_for(red),
                blue: self.building.get_score_for(blue)
            },
            "waiting_passengers": {
                red: {f: len(list(c)) for f, c in groupby(sorted(filter(lambda p: p.is_walking_on_floor(), self.get_red_passengers()), key=lambda p: p.floor), lambda p: p.floor)},
                blue: {f: len(list(c)) for f, c in groupby(sorted(filter(lambda p: p.is_walking_on_floor(), self.get_blue_passengers()), key=lambda p: p.floor), lambda p: p.floor)}
            }
        }

    def get_red_elevators(self):
        return self.building.get_player_elevator(settings.PLAYERS['FIRST_PLAYER_KEY'])

    def get_blue_elevators(self):
        return self.building.get_player_elevator(settings.PLAYERS['SECOND_PLAYER_KEY'])

    def get_red_passengers(self):
        return filter(lambda p: p.get_type() == settings.PLAYERS['FIRST_PLAYER_KEY'], self.get_passengers())

    def get_blue_passengers(self):
        return filter(lambda p: p.get_type() == settings.PLAYERS['SECOND_PLAYER_KEY'], self.get_passengers())

    def get_passengers(self):
        return self.building.all_passengers

    def get_state(self):
        red = settings.PLAYERS["FIRST_PLAYER_KEY"]
        blue = settings.PLAYERS["SECOND_PLAYER_KEY"]
        return {
            red + "_elevators": [e.serialize() for e in self.get_red_elevators()],
            blue + "_elevators": [e.serialize() for e in self.get_blue_elevators()],
            "passengers": [p.serialize() for p in self.get_passengers() if not p.is_walking_on_floor()],
            red + "_score": self.building.get_score_for(red),
            blue + "_score": self.building.get_score_for(blue)
        }
