package core.API

import org.json.simple.JSONObject

class Passenger(passenger: JSONObject) : MessagesInterface{

  val id: Int = passenger["id"]?.toString()?.toInt() ?: 0
  var elevator: Int = passenger["elevator"]?.toString()?.toInt() ?: 0
    private set

  val fromFloor: Int = passenger["from_floor"]?.toString()?.toInt() ?: 0
  val destFloor: Int = passenger["dest_floor"]?.toString()?.toInt() ?: 0
  val state: Int = passenger["state"]?.toString()?.toInt() ?: 0
  val timeToAway: Int = passenger["time_to_away"]?.toString()?.toInt() ?: 0
  val type: String = passenger["type"]?.toString() ?: ""
  val floor: Int = passenger["floor"]?.toString()?.toLong()?.toInt() ?: 0
  private val messages = ArrayList<JSONObject>()
  var x: Double = passenger["x"]?.toString()?.toDouble() ?: 0.0
  var y: Double = passenger["y"]?.toString()?.toDouble() ?: 0.0
  val weight: Double = passenger["weight"]?.toString()?.toDouble() ?: 1.0

  override fun getMessages(): List<JSONObject> = messages

  fun setElevator(elevator: Elevator) {
    this.elevator = elevator.id
    val jo = JSONObject()
    jo.put("command", "set_elevator_to_passenger")
    val args = JSONObject()
    args.put("passenger_id", this.id)
    args.put("elevator_id", elevator.id)
    jo.put("args", args)
    this.messages.add(jo)
  }
}