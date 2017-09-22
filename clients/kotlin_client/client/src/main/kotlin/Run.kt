import core.Client

fun main(args: Array<String>) {
  val host = System.getenv("WORLD_NAME") ?: "127.0.0.1"
  val solutionId = System.getenv("SOLUTION_ID") ?: "-1"
  val client = Client(host, 8000, solutionId)
  client.connect()
}