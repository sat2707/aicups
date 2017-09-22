```php
// В стратегию приходит четыре массива
$my_passengers: array из Passenger
$my_elevators: array из Elevator
$enemy_passengers: array из Passenger
$enemy_elevators: array из Elevator
// Для отладки в консоль используйте вызов
$this->log($text)
// Каждый тик вызывается Strategy->on_tick($my_passengers, $my_elevators,
$enemy_passengers, $enemy_elevators)
// API для работы с пассажирами
class Passenger {
    function __construct() {
        // Текущий этаж :integer
        $this->floor = $floor;
        // Этаж, с которого едет пассажир :integer
        $this->from_floor = $from_floor;
        // Этаж, на который едет пассажир :integer
        $this->dest_floor = $dest_floor;
        // Сколько времени осталось до ухода на лестницу :integer
        $this->time_to_away = $time_to_away;
        // Координаты пассажира :float
        $this->x = $x;
        $this->y = $y;
        // Узнать к какому игроку привязан пассажир :string {"FIRST_PLAYER",
"SECOND_PLAYER"}
        $this->type = $type;
        // Состояние пассажира
        $this->state = $state;
    }
    // Назначить пассажиру лифт
    public function set_elevator($elevator) {}
    // Проверяет, назначен ли лифт пассажиру
    public function has_elevator() : bool {}
}
// API для работы с лифтами
class Elevator {
    function __construct() {
        // Текущий этаж :integer
        $this->floor = $floor;
        // Этаж, к которому лифт едет в данный момент :integer
        $this->next_floor = $next_floor;
        // Сколько времени лифт простоял на этаже :integer
        $this->time_on_floor = $time_on_floor;
        // Координата лифта по Y :float
        $this->y = $y;
        // Скорость движения в текущий момент :float
        $this->speed = $speed;
        // Какому игроку принадлежит :string {"FIRST_PLAYER", "SECOND_PLAYER"}
        $this->type = $type;
        // Массив пассажиров, которых перевозит данный лифт
        $this->$passengers = $passengers;
        // Состояние лифта
        $this->state = $state;
}
    // Отправить лифт на указанный этаж, он доедет и выпустит
пассажиров :integer
    public function go_to_floor(floor) {}
}
```
