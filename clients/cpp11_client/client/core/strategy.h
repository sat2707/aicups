#include "base_strategy.h"
#include <vector>

class Strategy : public BaseStrategy
{
public:
    void on_tick(std::vector<Elevator>& myElevators, std::vector<Passenger>& myPassengers, std::vector<Elevator>& enemyElevators, std::vector<Passenger>& enemyPassengers) {
        for (auto& elevator : myElevators) {
            for (auto& passenger : myPassengers) {
                if (passenger.state < 5) {
                    if (elevator.state != 1) {
                        elevator.go_to_floor(passenger.from_floor);
                    }
                    if (elevator.floor == passenger.from_floor) {
                        passenger.set_elevator(elevator);
                    }
                }
            }
            if(elevator.passengers.size() > 0 && elevator.state != 1) {
                elevator.go_to_floor(elevator.passengers[0].dest_floor);
            }
        }
//        auto& elevator = elevators[0];
//        for (auto& passenger : passengers)
//            if (! passenger.has_elevator() && elevator.floors.size() == 0) {
//                elevator.floors_add_last({passenger.from_floor, passenger.dest_floor});
//                passenger.set_elevator(elevator);
//            }
    }
};
