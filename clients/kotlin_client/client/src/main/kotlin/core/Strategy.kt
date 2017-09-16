package core

import core.API.Elevator
import core.API.Passenger

class Strategy : BaseStrategy() {
  override fun onTick(myPassengers: List<Passenger>, myElevators: List<Elevator>, enemyPassengers: List<Passenger>, enemyElevators: List<Elevator>) {
    for (e in myElevators) {
      for (p in myPassengers) {
        if (p.state < 5) {
          if (e.state != 1) {
            e.goToFloor(p.fromFloor)
          }
          if (e.floor == p.fromFloor) {
            p.setElevator(e)
          }
        }
      }
      if (e.passengers.size > 0 && e.state != 1) {
        e.goToFloor(e.passengers[0].destFloor)
      }
    }
  }
}