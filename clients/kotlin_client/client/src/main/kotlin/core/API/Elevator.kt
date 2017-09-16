package core.API

import org.json.simple.JSONArray
import org.json.simple.JSONObject

class Elevator(elevator: JSONObject) : MessagesInterface {
  val id: Int = elevator["id"]?.toString()?.toInt() ?: 0
  val y: Double = elevator["y"]?.toString()?.toDouble() ?: 0.0
  val passengers = ArrayList<Passenger>()
  val state: Int = elevator["state"]?.toString()?.toInt() ?: 0
  val speed: Double = elevator["speed"]?.toString()?.toDouble() ?: 0.0
  val timeOnFloor: Int = elevator["time_on_floor"]?.toString()?.toInt() ?: 0
  val floor: Int = elevator["floor"]?.toString()?.toInt() ?: 0
  val type: String = elevator["type"]?.toString() ?: ""
  var nextFloor: Int = elevator["next_floor"]?.toString()?.toInt() ?: 0
    private set
  val messages = ArrayList<JSONObject>()

  init {
    (elevator["passengers"] as JSONArray).mapTo(passengers) { Passenger(it as JSONObject) }
  }

  override fun getMessages(): List<JSONObject> = messages

  fun goToFloor(floor: Int?) {
    this.nextFloor = floor ?: 0
    val jo = JSONObject()
    jo.put("command", "go_to_floor")
    val args = JSONObject()
    args.put("elevator_id", this.id)
    args.put("floor", floor)
    jo.put("args", args)
    this.messages.add(jo)
  }
}