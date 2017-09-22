package core.API

import core.BaseStrategy
import core.Strategy
import javafx.util.Pair
import org.json.simple.JSONArray
import org.json.simple.JSONObject
import java.util.ArrayList
import java.util.function.Function
import java.util.stream.Collectors
import java.util.stream.Stream

class API {
  private val debug = Debug()
  private var strategy : BaseStrategy? = null

  init {
    try {
      strategy = Strategy()
      strategy?.setDebug(debug)
    } catch (e: Exception) {
      debug.exception(e)
    }
  }

  private fun parseState(state: JSONObject): Pair<Pair<List<Passenger>, List<Elevator>>, Pair<List<Passenger>, List<Elevator>>> {
    val myPassengers = (state["my_passengers"] as JSONArray).map { Passenger(it as JSONObject) }
    val myElevators = (state["my_elevators"] as JSONArray).mapTo(ArrayList(3)) { Elevator(it as JSONObject) }

    val enemyPassengers = (state["enemy_passengers"] as JSONArray).map { Passenger(it as JSONObject) }
    val enemyElevators = (state["enemy_elevators"] as JSONArray).mapTo(ArrayList(3)) { Elevator(it as JSONObject) }

    val myPair = Pair<List<Passenger>, List<Elevator>>(myPassengers, myElevators)
    val enemyPair = Pair<List<Passenger>, List<Elevator>>(enemyPassengers, enemyElevators)

    return Pair(myPair, enemyPair)
  }

  fun turn(state: JSONObject): JSONArray {
    val pair = parseState(state)

    try {
      this.strategy?.onTick(pair.key.key, pair.key.value, pair.value.key, pair.value.value)
    } catch (e: Exception) {
      debug.exception(e)
    }

    val resultArray = JSONArray()
    resultArray.addAll(Stream.of(pair.key.key.stream(),
        pair.key.value.stream(),
        pair.value.key.stream(), Stream.of(debug))
        .flatMap(Function.identity())
        .flatMap { msg -> msg.getMessages().stream() }
        .collect(Collectors.toList()))
    return resultArray
  }
}