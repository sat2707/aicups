```python
# В стратегию приходит четыре массива
list из Elevator: my_elevators
list из Passenger: my_passengers
list из Elevator: enemy_elevators
list из Passenger: enemy_passengers
# Для отладки в консоль используйте вызов
self.debug(str)
# Каждый тик вызывается Strategy.on_tick(my_elevators, my_passengers,
enemy_elevators, enemy_passengers)
# API для работы с пассажирами
class Passenger(object):
    def __init__(self, x, y, type, time_to_away, from_floor, dest_floor,
floor):
# Текущий этаж :int
self.floor = floor
# Этаж, с которого едет пассажир: int
self.from_floor = from_floor
# Этаж, на который едет пассажир :int
self.dest_floor = dest_floor
# Сколько времени осталось до ухода на лестницу :int
self.time_to_away = time_to_away
# Координаты пассажира :float
self.x, self.y = x, y
# Узнать к какому игроку привязан пассажир :string
# Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
self.type = type
# Состояние пассажира
self.state = state
    # Проверяет, назначен ли лифт пассажиру
    def has_elevator(self): pass
    # Назначить пассажиру лифт
    def set_elevator(self, elevator): pass
# API для работы с лифтами
class Elevator(object):
    def __init__(self, y, passengers, speed, floor, next_floor, time_on_floor,
type):
# Текущий этаж :int
self.floor = floor
# Этаж, к которому лифт едет в данный момент :int
self.next_floor = next_floor
# Сколько времени лифт простоял на этаже :int
self.time_on_floor = time_on_floor
# Координата лифта по Y :float
self.y = y
# Скорость движения в текущий момент :float
self.speed = speed
# Какому игроку принадлежит :string
# Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
self.type = type
# Массив пассажиров, которых перевозит данный лифт :list из Passenger
self.passengers = passengers
# Состояние лифта
self.state = state
# Отправить лифт на указанный этаж :int, он доедет и выпустит пассажиров
def go_to_floor(self, floor): pass
```
