import Foundation

class Strategy: BaseStrategy {
  let debug:Debug
  required init(debug:Debug)
  {
    self.debug = debug
  }
  func onTick(myElevators:[Elevator], enemyElevators:[Elevator], myPassenger:[Passenger], enemyPassenger: [Passenger]) {
    myElevators.forEach({ elevator in
      myPassenger.forEach({
        if $0.state.rawValue < 5{
          if elevator.state != .moving
          {
            elevator.go(toFloor: $0.fromFloor)
          }
          if elevator.floor == $0.fromFloor
          {
            $0.set(elevator: elevator)
          }
        }
      })
      if !elevator.passengers.isEmpty && elevator.state != .moving{
        elevator.go(toFloor: elevator.passengers.first!.destFloor)
      }
    })
  }
}
