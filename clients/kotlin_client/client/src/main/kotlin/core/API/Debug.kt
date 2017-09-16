package core.API

import org.json.simple.JSONObject
import java.util.*

class Debug : MessagesInterface {

  private var messages = ArrayList<JSONObject>()

  fun log(obj: Any) {
    val jo = JSONObject()
    jo.put("command", "log")

    val args = JSONObject()
    args.put("text", obj.toString())

    jo.put("args", args)
    this.messages.add(jo)
  }

  fun exception(obj: Any) {
    val jo = JSONObject()
    jo.put("command", "exception")

    val args = JSONObject()
    args.put("text", obj.toString())

    jo.put("args", args)
    this.messages.add(jo)
  }


  override fun getMessages(): List<JSONObject> {
    val result = ArrayList(this.messages)
    this.messages.clear()
    return result
  }

}