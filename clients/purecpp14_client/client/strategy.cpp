#include "strategy.h"
#include <iostream>

std::ostream & operator << (std::ostream &s, const Elevator &e)
{
	s << "Elevator(id=" << e.id << ")";
	return s;
}

std::ostream & operator << (std::ostream &s, const Passenger &p)
{
	s << "Passenger(id=" << p.id << ")";
	return s;
}

void Strategy::on_tick(const std::vector<Elevator>& myElevators,
                       const std::vector<Passenger>& myPassengers,
                       const std::vector<Elevator>& enemyElevators,
                       const std::vector<Passenger>& enemyPassengers)
{
    for (auto& elevator : myElevators)
    {
        for (auto& passenger : myPassengers)
        {
            if (passenger.state < 5)
            {
                if (elevator.state != 1)
                {
                    elevator.go_to_floor(passenger.from_floor);
                }
                if (elevator.floor == passenger.from_floor)
                {
                    passenger.set_elevator(elevator);
                }
            }
        }
        if(elevator.passengers.size() > 0 && elevator.state != 1)
        {
            elevator.go_to_floor(elevator.passengers[0].dest_floor);
        }
    }

    log() << "Hello " << myElevators[0];
}

