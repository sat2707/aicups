import Foundation

protocol Debug {
  func log(object:AnyObject)
  func `extension`(object:AnyObject)
}
protocol BaseStrategy {
  init(debug:Debug)
  func onTick(myElevators:[Elevator], enemyElevators:[Elevator], myPassenger:[Passenger], enemyPassenger: [Passenger])
}
