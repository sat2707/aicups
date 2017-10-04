package main

import (
	"github.com/pomkac/aicups/clients/go_client/client/core/API"
)

type Strategy struct {
	API.BaseStrategy
}

// Вызывается при инициализации клиента
func (s *Strategy) Init(){

}

func (s *Strategy) OnTick(myPassengers []*API.Passenger, myElevators []*API.Elevator,
				enemyPassengers []*API.Passenger, enemyElevators []*API.Elevator) error {

	for i := 0; i < len(myElevators); i++ {
		elevator := myElevators[i]

		for j := 0; j < len(myPassengers); j++ {
			passenger := myPassengers[j]

			if passenger.State() < 5{
				if elevator.State() != 1{
					elevator.GoToFloor(passenger.FromFloor())
				}
				if elevator.Floor() == passenger.Floor(){
					passenger.SetElevator(elevator)
				}
			}
		}

		if len(elevator.Passengers()) > 0 && elevator.State() != 1{
			elevator.GoToFloor(elevator.Passengers()[0].DestFloor())
		}
	}

	return nil
}

