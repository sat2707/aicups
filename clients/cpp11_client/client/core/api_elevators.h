#ifndef API_ELEVATORS_H
#define API_ELEVATORS_H

#include "base_strategy.h"
#include "strategy.h"

class API_Elevators : public QObject
{
    Q_OBJECT

private:
    Strategy strategy;

public:
    API_Elevators() : strategy(Strategy()) {}

private slots:
    void generateActions(QJsonObject data) {
        QJsonArray actions;
        Adder addAction = [&actions] (const QString& action, const QJsonValue& value) {
            QJsonObject jsonAction;
            jsonAction.insert("command", action);
            jsonAction.insert("args", value);
            actions.append(QJsonValue(jsonAction));
        };

        Adder dummyAction = [&actions] (const QString& action, const QJsonValue& value) {

        };

        QJsonValue myElevatorsData = data.take("my_elevators");
        vector<Elevator> myElevators;
        convertJsonToVector<>(myElevatorsData, myElevators, addAction);

        QJsonValue myPassengersData = data.take("my_passengers");
        vector<Passenger> myPassengers;
        convertJsonToVector<>(myPassengersData, myPassengers, addAction);

        QJsonValue enemyElevatorsData = data.take("enemy_elevators");
        vector<Elevator> enemyElevators;
        convertJsonToVector<>(enemyElevatorsData, enemyElevators, dummyAction);

        QJsonValue enemyPassengersData = data.take("enemy_passengers");
        vector<Passenger> enemyPassengers;
        convertJsonToVector<>(enemyPassengersData, enemyPassengers, addAction);

        Debug debug(addAction);
        try {
            strategy.set_debug(debug);
            strategy.on_tick(myElevators, myPassengers, enemyElevators, enemyPassengers);
        }
        catch (const std::exception& e) {
            debug.exception(e);
        }
        emit sendActions(actions);
    }

signals:
    void sendActions(QJsonArray);
};

#endif // API_ELEVATORS_H

