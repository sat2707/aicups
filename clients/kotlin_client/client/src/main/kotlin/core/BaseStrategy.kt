package core

import core.API.Debug
import core.API.Elevator
import core.API.Passenger

open class BaseStrategy {
  private var debug: Debug? = null

  fun setDebug(debug: Debug) {
    this.debug = debug
  }
  fun log(obj: Any) = debug?.log(obj)
  open fun onTick(myPassengers: List<Passenger>, myElevators: List<Elevator>, enemyPassengers: List<Passenger>, enemyElevators: List<Elevator>) {}
}