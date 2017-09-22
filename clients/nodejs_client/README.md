```javascript
// В стратегию приходит четыре массива
Array из Elevator myElevators
Array из Passenger myPassengers
Array из Elevator enemyElevators
Array из Passenger enemyPassengers
// Для отладки в консоль используйте вызов
this.debug(String)
// Каждый тик вызывается Strategy.onTick(myPassengers, myElevators,
enemyPassengers, enemyElevators)
// API для работы с пассажирами
class Passenger {
    // Назначить пассажиру лифт
    setElevator(elevator) {}
    // Проверяет, назначен ли лифт пассажиру :Boolean
    hasElevator() {}
    // Текущий этаж :Number
    get floor() {}
    // Этаж, с которого едет пассажир :Number
    get fromFloor() {}
    // Этаж, на который едет пассажир :Number
    get destFloor() {}
    // Сколько времени осталось до ухода на лестницу :Number
    get timeToAway() {}
    // Координаты пассажира :Number
    get x() {}
    get y() {}
    // Узнать к какому игроку привязан пассажир :String
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    get type() {}
    // Состояние пассажира
    get state() {}
}
// API для работы с лифтами
class Elevator {
    // Отправить лифт на указанный этаж, он доедет и выпустит
пассажиров :Number
    go_to_floor(floor) {}
    // Массив пассажиров, которых перевозит данный лифт :Array
    get passengers() {}
    // Текущий этаж :Number
    get floor() {}
    // Этаж, к которому лифт едет в данный момент :Number
    get nextFloor() {}
    // Сколько времени лифт простоял на этаже :Number
    get timeOnFloor() {}
    // Координата лифта по Y :Number
get y() {}
    // Скорость движения в текущий момент :Number
    get speed() {}
    // Какому игроку принадлежит :String
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    get type() {}
    // Состояние лифта
    get state() {}
}
```
