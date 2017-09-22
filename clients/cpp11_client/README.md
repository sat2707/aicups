```cpp
// В стратегию приходят ссылки четыре массива
std::vector<Elevator>& myElevators;
std::vector<Passenger>& myPassengers;
std::vector<Elevator>& enemyElevators;
std::vector<Passenger>& enemyPassengers;
// Для отладки в консоль используйте вызов this->log(T smth)
// Допустимы типы: bool, int, short, long, float, double, char, QString,
Passenger, Elevator
// Каждый тик вызывается strategy->onTick(List<Passenger>, List<Elevator>,
List<Passenger>, List<Elevator>)
// API для работы с пассажирами
class Passenger {
public:
    // Текущий этаж
    int floor;
    // Этаж, с которого едет пассажир
    int from_floor;
    // Этаж, на который едет пассажир
    int dest_floor;
    // Координаты пассажира
    int x, y;
    // Сколько времени осталось до ухода на лестницу
    int time_to_away;
    // Состояние пассажира
    int state;
    // Узнать к какому игроку привязан пассажир
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    QString type;
public:
    // проверить, есть ли у пассажира лифт
     bool has_elevator() {}
    // назначить пассажиру лифт
    void set_elevator(const Elevator& elevator) {}
};
// API для работы с лифтами
class Elevator {
public:
    // Текущий этаж
    int floor;
    // Этаж, к которому лифт едет в данный момент
    int next_floor;
    // Сколько времени лифт простоял на этаже
    int time_on_floor;
    // Координата лифта по Y
    double y;
    // Скорость движения в текущий момент
    double speed;
    // Какому игроку принадлежит
    // Возвращаемое значение "FIRST_PLAYER", "SECOND_PLAYER"
    QString type;
    // Состояние лифта
    int state;
    // Массив пассажиров, которых перевозит данный лифт
    std::vector<Passenger> passengers;
public:
     // Отправить лифт на указанный этаж, он доедет и выпустит пассажиров
    void go_to_floor(int floor) {}
};
```
