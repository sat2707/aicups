package core.API

import org.json.simple.JSONObject

interface MessagesInterface {
  fun getMessages(): List<JSONObject>
}