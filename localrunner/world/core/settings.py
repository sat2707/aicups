from random import randint, seed
import sys

try:
    sd = int(sys.argv[1])
except (ValueError, TypeError, IndexError):
    sd = randint(0, 10**12)

seed(sd)

PLAYERS = {
    "FIRST_PLAYER_KEY": "FIRST_PLAYER",
    "SECOND_PLAYER_KEY": "SECOND_PLAYER"
}

BUILDING = {
    'TICK_TO_SPAWN': 20,
    'TICK_COUNT_TO_SPAWN': 2000,
    'FLOORS_QUEUE_LEN': lambda: randint(1, 5),
}

BUILDING_VISIO = {
    'PASSENGER_SPAWN_POSITION': 20,
    'ELEVATORS_FOR_PASSENGER_COUNT': 4,
    'FIRST_ELEVATOR_POSITION': 60,
    'ELEVATOR_IN_GROUP_OFFSET': 80,
    'LADDER_POSITION': 400,
    'FLOORS_COUNT': 9,
    'FIRST_FLOOR': 1,
    'INDICATOR_POSITION': 350,
    'SEED': sd
}

BUILDING.update(BUILDING_VISIO)

ELEVATORS = {
    'TICKS_PER_FLOOR': 50,
    'OPENING_TICKS': 100,
    'CLOSING_TICKS': 100,
    'SOFT_CAPACITY': 10,
    'FILLING_DELAY': 40,
    'TIME_ON_THE_FLOOR_TO_LOAD_ENEMY_PASSENGER': 40,
    'OVERLOAD_MULTIPLY': 1.1,
    'CRITICAL_CAPACITY': 20,
    'SPEED': 2,
}

PASSENGERS = {
    'SPEED': {
        'HORIZONTAL': 2,
        'DOWN': 100,
        'UP': 200,
    },
    'WEIGHT': lambda: randint(1010000, 1030000) / 1000000.,
    'REWARD': 10,
    'ENEMY_REWARD': 2,
    'TIME_TO_AWAY': 500,
    'WALKING_TIME': 500,
    'MOVE_TO_FLOOR': 40,
}
