package API

type Passenger struct {
	message
	mID         int
	mState      int
	mType       string
	mFloor      int
	mX          int
	mY          int
	mElevator   int
	mFromFloor  int
	mDestFloor  int
	mTimeToAway int
}

func (p *Passenger) ID() int {
	return p.mID
}

func (p *Passenger) State() int {
	return p.mState
}

func (p *Passenger) Type() string {
	return p.mType
}

func (p *Passenger) Floor() int {
	return p.mFloor
}

func (p *Passenger) X() int {
	return p.mX
}

func (p *Passenger) Y() int {
	return p.mY
}

func (p *Passenger) HasElevator() bool {
	return p.mElevator != -1
}

func (p *Passenger) FromFloor() int {
	return p.mFromFloor
}

func (p *Passenger) DestFloor() int {
	return p.mDestFloor
}

func (p *Passenger) TimeToAway() int {
	return p.mTimeToAway
}

func (p *Passenger) SetElevator(elevator *Elevator) {
	p.mElevator = elevator.ID()

	cmd := make(map[string]interface{})
	cmd["passenger_id"] = p.ID()
	cmd["elevator_id"] = elevator.ID()

	message := make(map[string]interface{})
	message["command"] = "set_elevator_to_passenger"
	message["args"] = cmd

	p.mMessages = append(p.mMessages, message)
}

func NewPassenger(JSONObj map[string]interface{}) *Passenger {
	p := &Passenger{}

	id, _ := JSONObj["id"]
	p.mID = int(id.(float64))

	state, _ := JSONObj["state"]
	p.mState = int(state.(float64))

	t, _ := JSONObj["type"]
	p.mType = t.(string)

	floor, _ := JSONObj["floor"]
	p.mFloor = int(floor.(float64))

	x, _ := JSONObj["x"]
	p.mX = int(x.(float64))

	y, _ := JSONObj["y"]
	p.mY = int(y.(float64))

	elevator, ok := JSONObj["elevator"]
	if !ok || elevator == nil {
		p.mElevator = -1
	} else {
		p.mElevator = int(elevator.(float64))
	}

	fromFloor, _ := JSONObj["from_floor"]
	p.mFromFloor = int(fromFloor.(float64))

	destFloor, _ := JSONObj["dest_floor"]
	p.mDestFloor = int(destFloor.(float64))

	timeToAway, _ := JSONObj["time_to_away"]
	p.mTimeToAway = int(timeToAway.(float64))

	return p
}
