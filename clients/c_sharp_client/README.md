```csharp
// В стратегию приходит четыре массива
List<Elevator> myElevators;
List<Passenger> myPassengers;
List<Elevator> enemyElevators;
List<Passenger> enemyPassengers;
// Для отладки в консоль используйте вызов
this.log(Object object)
// Каждый тик вызывается Strategy.onTick(List<Passenger>, List<Elevator>, List<Passenger>, List<Elevator>)
// API для работы с пассажирами
class Passenger {
    // Назначить пассажиру лифт
    public void SetElevator(Elevator elevator) {}
    // Проверяет, назначен ли лифт пассажиру
    public bool HasElevator() {}
    // Текущий этаж
    public int Floor;
    // Этаж, с которого едет пассажир
    public int FromFloor;
    // Этаж, на который едет пассажир
    public int DestFloor;
    // Состояние пассажира
    public int State;
    // Сколько времени осталось до ухода на лестницу
    public int TimeToAway;
    // Координаты пассажира
    public float Y;
    public float X;
    // Узнать к какому игроку привязан пассажир
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    public String Type;
    // Вес пассажира
    public float Weight;
}
// API для работы с лифтами
class Elevator {
    // Отправить лифт на указанный этаж, он доедет и выпустит пассажиров
    public void goToFloor(int floor) {}
    // Массив пассажиров, которых перевозит данный лифт
    public List<Passenger> Passengers;
    // Текущий этаж
    public int Floor;
    // Этаж, к которому лифт едет в данный момент
    public int NextFloor;
    // Сколько времени лифт простоял на этаже
    public int TimeOnFloor;
    // Координата лифта по Y
    public float Y;
    // Скорость движения в текущий момент
    public float Speed;
    // Какому игроку принадлежит
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    public String Type;
    // Состояние Лифта
    public int State;
}
```
