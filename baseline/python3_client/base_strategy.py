class BaseStrategy(object):
    debug = None

    def set_debug(self, debug):
        self.debug = debug.log

    def on_tick(self, passengers, elevators):
        pass
