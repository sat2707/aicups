package API

type Elevator struct {
	message
	mID          int
	mState       int
	mType        string
	mFloor       int
	mY           float64
	mPassengers  []*Passenger
	mSpeed       float64
	mTimeOnFloor int
	mNextFloor   int
}

func (e *Elevator) ID() int {
	return e.mID
}

func (e *Elevator) State() int {
	return e.mState
}

func (e *Elevator) Type() string {
	return e.mType
}

func (e *Elevator) Floor() int {
	return e.mFloor
}

func (e *Elevator) Y() float64 {
	return e.mY
}

func (e *Elevator) Passengers() []*Passenger {
	return e.mPassengers
}

func (e *Elevator) Speed() float64 {
	return e.mSpeed
}

func (e *Elevator) TimeOnFloor() int {
	return e.mTimeOnFloor
}

func (e *Elevator) NextFloor() int {
	return e.mNextFloor
}

func (e *Elevator) GoToFloor(floor int) {
	e.mNextFloor = floor

	cmd := make(map[string]interface{})
	cmd["elevator_id"] = e.ID()
	cmd["floor"] = floor

	message := make(map[string]interface{})
	message["command"] = "go_to_floor"
	message["args"] = cmd

	e.mMessages = append(e.mMessages, message)
}

func NewElevator(JSONObj map[string]interface{}) *Elevator {

	e := &Elevator{}

	id, _ := JSONObj["id"]
	e.mID = int(id.(float64))

	state, _ := JSONObj["state"]
	e.mState = int(state.(float64))

	t, _ := JSONObj["type"]
	e.mType = t.(string)

	floor, _ := JSONObj["floor"]
	e.mFloor = int(floor.(float64))

	y, _ := JSONObj["y"]
	e.mY = y.(float64)

	passengers, _ := JSONObj["passengers"]

	for _, passenger := range passengers.([]interface{}) {
		e.mPassengers = append(e.Passengers(), NewPassenger(passenger.(map[string]interface{})))
	}

	speed, _ := JSONObj["speed"]
	e.mSpeed = speed.(float64)

	timeOnFloor, _ := JSONObj["time_on_floor"]
	e.mTimeOnFloor = int(timeOnFloor.(float64))

	nextFloor, _ := JSONObj["next_floor"]
	e.mNextFloor = int(nextFloor.(float64))

	return e
}
