#ifndef STRATEGY_H
#define STRATEGY_H

#include <vector>
#include "base_strategy.h"
#include "api.h"

class Strategy : public BaseStrategy
{
public:
    void on_tick(const std::vector<Elevator>& myElevators,
                 const std::vector<Passenger>& myPassengers,
                 const std::vector<Elevator>& enemyElevators,
                 const std::vector<Passenger>& enemyPassengers);
};

#endif
