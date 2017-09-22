package API

type BaseStrategy struct {
	mDebug *Debug
}

type IBaseStrategy interface {
	Init()
	Debug() *Debug
	SetDebug(debug *Debug)
	Log(object interface{})
	OnTick(myPassengers []*Passenger, myElevators []*Elevator,
		enemyPassengers []*Passenger, enemyElevators []*Elevator) error
}

func (s *BaseStrategy) Init() {

}

func (s *BaseStrategy) Debug() *Debug {
	return s.mDebug
}

func (s *BaseStrategy) SetDebug(debug *Debug) {
	s.mDebug = debug
}

func (s *BaseStrategy) Log(object interface{}) {
	s.mDebug.Log(object)
}

func (s *BaseStrategy) OnTick(myPassengers []*Passenger, myElevators []*Elevator,
	enemyPassengers []*Passenger, enemyElevators []*Elevator) error {

	return nil
}
