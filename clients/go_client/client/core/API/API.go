package API

type API struct {
	mDebug    *Debug
	mStrategy  IBaseStrategy
}

func (a *API) parseState(state map[string]interface{}) ([]*Passenger, []*Elevator, []*Passenger, []*Elevator) {

	var myPassengers, enemyPassengers []*Passenger
	var myElevators, enemyElevators []*Elevator

	my_passengers, _ := state["my_passengers"]

	for _, passenger := range my_passengers.([]interface{}) {
		myPassengers = append(myPassengers, NewPassenger(passenger.(map[string]interface{})))
	}

	enemy_passengers, _ := state["enemy_passengers"]

	for _, passenger := range enemy_passengers.([]interface{}) {
		enemyPassengers = append(enemyPassengers, NewPassenger(passenger.(map[string]interface{})))
	}

	my_elevators, _ := state["my_elevators"]

	for _, elevator := range my_elevators.([]interface{}) {
		myElevators = append(myElevators, NewElevator(elevator.(map[string]interface{})))
	}

	enemy_elevators, _ := state["enemy_elevators"]

	for _, elevator := range enemy_elevators.([]interface{}) {
		enemyElevators = append(enemyElevators, NewElevator(elevator.(map[string]interface{})))
	}

	return myPassengers, myElevators, enemyPassengers, enemyElevators
}

func (a *API) Turn(state map[string]interface{}) []interface{}{
	messages := []interface{}{}

	myPassengers, myElevators, enemyPassengers, enemyElevators := a.parseState(state)

	err := a.mStrategy.OnTick(myPassengers, myElevators, enemyPassengers, enemyElevators)

	if err != nil{
		a.mDebug.Exception(err)
	}

	for i := 0; i < len(myPassengers); i++ {
		if m := myPassengers[i].Messages(); m != nil{
			messages = append(messages, m...)
		}
	}

	for i := 0; i < len(myElevators); i++ {
		if m := myElevators[i].Messages(); m != nil{
			messages = append(messages, m...)
		}
	}

	for i := 0; i < len(enemyPassengers); i++ {
		if m := enemyPassengers[i].Messages(); m != nil{
			messages = append(messages, m...)
		}
	}

	for i := 0; i < len(enemyElevators); i++ {
		if m := enemyElevators[i].Messages(); m != nil{
			messages = append(messages, m...)
		}
	}

	if m := a.mDebug.Messages(); m != nil{
		messages = append(messages, m...)
	}

	return messages
}

func NewAPI(s IBaseStrategy) *API {
	a := &API{}
	a.mDebug = NewDebug()
	a.mStrategy = s
	a.mStrategy.Init()
	a.mStrategy.SetDebug(a.mDebug)

	return a
}