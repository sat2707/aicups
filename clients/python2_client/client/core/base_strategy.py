class BaseStrategy(object):
    def __init__(self, debug, type):
        self.debug = debug.log
        self.type = type

    def on_tick(self, my_elevators, my_passengers, enemy_elevators, enemy_passengers):
       pass