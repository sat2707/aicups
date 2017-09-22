#ifndef API_H
#define API_H

#include <QJsonObject>
#include <QJsonArray>
#include <QJsonValue>
#include <QJsonDocument>
#include <functional>
#include <QDebug>

using std::vector;
using std::function;
typedef function<void(const QString&, const QJsonValue&)> Adder;

template <typename T>
void convertJsonToVector(const QJsonValue& data, vector<T>& result, const Adder& addAction) {
    if (data.isArray()) {
        QJsonArray dataArray = data.toArray();
        for (QJsonValue item : dataArray) {
            result.push_back(T(item, addAction));
        }
    }
}

template <typename T>
QJsonArray convertVectorToJson(const vector<T>& data) {
    QJsonArray result;
    for (const T& item : data) {
        result.append(QJsonValue(item));
    }
    return result;
}

class Passenger;

// (Лифт) атрибуты только на чтение!!
class Elevator {
public:
    int id;
    double y;
    vector<Passenger> passengers;
    double speed;
    int time_on_floor;
    int next_floor;
    QString type;
    int floor;
    int state;
    Adder adder;

public:
    Elevator(const QJsonValue& data, const Adder& _adder) : adder(_adder) {
        QJsonObject json = data.toObject();
        id = json.take("id").toInt();
        y = json.take("y").toDouble();
        convertJsonToVector<>(json.take("passengers"), passengers, adder);

        speed = json.take("speed").toDouble();
        time_on_floor = json.take("time_on_floor").toInt();
        next_floor = json.take("next_floor").toInt();
        type = json.take("type").toString();
        floor = json.take("floor").toInt();

        state = json.take("state").toInt(-1);
    }
    void go_to_floor(int floor) {
        next_floor = floor;
        QJsonObject args;
        args.insert("elevator_id", id);
        args.insert("floor", floor);
        adder("go_to_floor", QJsonValue(args));
    }
};



// (Пассажир) атрибуты только на чтение!!
class Passenger {
public:
    int id;             // идентификатор
    double x, y;           // координаты
    int from_floor, dest_floor; // этаж появления и цели
    int time_to_away;
    QString type;
    int floor;
    int elevator;    // идентификатор назначенного лифта
    int state;
    Adder adder;

public:
    Passenger(const QJsonValue& data, const Adder& _adder) : adder(_adder) {
        QJsonObject json = data.toObject();
        id = json.take("id").toInt();
        x = json.take("x").toDouble();
        y = json.take("y").toDouble();
        from_floor = json.take("from_floor").toInt();
        dest_floor = json.take("dest_floor").toInt();
        time_to_away = json.take("time_to_away").toInt();
        type = json.take("type").toString();
        elevator = json.take("elevator").toInt();
        state = json.take("state").toInt();
    }

    bool has_elevator() {
        return elevator != -1;
    }

    void set_elevator(const Elevator& elevator) {
        this->elevator = elevator.id;
        QJsonObject args;
        args.insert("passenger_id", id);
        args.insert("elevator_id", elevator.id);
        adder("set_elevator_to_passenger", QJsonValue(args));
    }
};


class Debug {
private:
    Adder adder;

private:
    QString toString(bool smth) { return QVariant(smth).toString(); }

    QString toString(int smth) { return QString::number(smth); }
    QString toString(short smth) { return QString::number(smth); }
    QString toString(long smth) { return QString::number(smth); }
    QString toString(unsigned smth) { return QString::number(smth); }
    QString toString(long unsigned smth) { return QString::number(smth); }
    QString toString(short unsigned smth) { return QString::number(smth); }

    QString toString(float smth) { return QString::number(smth); }
    QString toString(double smth) { return QString::number(smth); }

    QString toString(char smth) { return QString(smth); }
    QString toString(QString smth) { return QString(smth); }
    QString toString(Passenger& smth) { return "Passenger id=" + toString(smth.id); }
    QString toString(Elevator& smth) { return "Elevator id=" + toString(smth.id); }

    template<typename T>
    QString toString(std::vector<T>& smth) {
        QString result = "{";
        for (auto item : smth) {
            result += toString(item) + ",";
        }
        return result + "}";
    }

public:
    Debug(const Adder& _adder) : adder(_adder) {}

    // Отладка в консоль (пригодится!)
    template<typename T>
    void log(T smth) {
        QJsonObject args;
        args.insert("text", toString(smth));
        adder("log", QJsonValue(args));
    }
    void exception(const std::exception& error) {
        QJsonObject args;
        args.insert("text", QString(error.what()));
        adder("exception", QJsonValue(args));
    }
};

#endif // API_H
