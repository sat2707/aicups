package core

import core.API.API
import org.json.simple.JSONAware
import org.json.simple.JSONObject
import org.json.simple.parser.ParseException
import org.json.simple.parser.JSONParser

import java.io.*
import java.net.InetSocketAddress
import java.nio.ByteBuffer
import java.nio.channels.SocketChannel

class Client(private val host: String, private val port: Int, private val solutionId: String) {
  private val parser = JSONParser()
  private var clientSocket: SocketChannel? = null

  private fun parseString(jsonString: String?): JSONObject? {
    if (jsonString == null) {
      return null
    }
    
    return try {
      parser.parse(jsonString) as JSONObject
    } catch (e: ParseException) {
      null
    }
  }

  @Throws(IOException::class)
  fun connect() {
    this.clientSocket = SocketChannel.open(InetSocketAddress(this.host, port))
    val obj = JSONObject()
    obj.put("solution_id", solutionId)
    clientSocket?.write(ByteBuffer.wrap(this.dumpMessage(obj).toByteArray()))

    val reader = BufferedReader(InputStreamReader(clientSocket?.socket()?.getInputStream()))
    val message = parseString(reader.readLine())
    if (message == null) {
      System.exit(1)
      return
    }
    if ("beginning" == message["message"]) {
      strategyLoop(reader)
    }
  }

  @Throws(IOException::class)
  private fun strategyLoop(reader: BufferedReader) {
    val api = API()
    while (true) {
      val obj = parseString(reader.readLine())
      if (obj == null || (obj["message"] != null && obj["message"] == "down")) {
        break
      }
      clientSocket?.write(ByteBuffer.wrap(this.dumpMessage(api.turn(obj)).toByteArray()))
    }
  }

  private fun dumpMessage(obj: JSONAware): String {
    return obj.toJSONString() + "\n"
  }
}