```java
// В стратегию приходит четыре массива
ArrayList<Elevator> myElevators;
ArrayList<Passenger> myPassengers;
ArrayList<Elevator> enemyElevators;
ArrayList<Passenger> enemyPassengers;
// Для отладки в консоль используйте вызов
this.log(Object object)
// Каждый тик вызывается Strategy.onTick(List<Passenger>, List<Elevator>,
List<Passenger>, List<Elevator>)
// API для работы с пассажирами
class Passenger {
    // Назначить пассажиру лифт
    public void setElevator(Elevator elevator) {}
    // Проверяет, назначен ли лифт пассажиру
    public Boolean hasElevator() {}
    // Текущий этаж
    public Integer getFloor() {}
    // Этаж, с которого едет пассажир
    public Integer getFromFloor() {}
    // Этаж, на который едет пассажир
    public Integer getDestFloor() {}
    // Состояние пассажира
    public Integer getState() {}
    // Сколько времени осталось до ухода на лестницу
    public Integer getTimeToAway() {}
    // Координаты пассажира
    public Double getY() {}
    public Double getX() {}
    // Узнать к какому игроку привязан пассажир
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    public String getType() {}
}
// API для работы с лифтами
class Elevator {
    // Отправить лифт на указанный этаж, он доедет и выпустит пассажиров
    public void goToFloor(Integer floor) {}
    // Массив пассажиров, которых перевозит данный лифт
    public List<Passenger> getPassengers() {}
    // Текущий этаж
    public Integer getFloor() {}
    // Этаж, к которому лифт едет в данный момент
    public Integer getNextFloor() {}
    // Сколько времени лифт простоял на этаже
    public Integer getTimeOnFloor() {}
    // Координата лифта по Y
    public Double getY() {}
    // Скорость движения в текущий момент
    public Double getSpeed() {}
    // Какому игроку принадлежит
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    public String getType() {}
    // Состояние Лифта
    public Integer getState() {}
}
```
