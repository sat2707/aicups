import Foundation

class Client {
  let socket:Socket
  let solutionID: Int
  let strategy: BaseStrategy
  let debug = DebugLog()
  init(host:String, port: Int, solutionID: Int) {
    socket = Socket(host: host, port: port)
    self.solutionID = solutionID
    strategy = Strategy(debug: debug)
  }
  
  func run()  {
    let decoder = JSONDecoder()
    let encoder = JSONEncoder()
    try! socket.connect()
    socket.write(data: "{\"solution_id\":  \(solutionID)}\n".data(using: .utf8)!)
    
    guard let data = socket.readLine() else {
      print("Can't read data")
      return
      
    }
    
    let _ = try! decoder.decode(FirstMessage.self, from: data)

    while true{
      guard let data = socket.readLine() else {
        print("Can't read data")
        break
      }
      do {
        let state = try decoder.decode(WorldState.self, from: data)
        strategy.onTick(myElevators: state.myElevators, enemyElevators: state.enemyElevators, myPassenger: state.myPassenger, enemyPassenger: state.enemyPassenger)
        
        
        var messagesToSend = [Message]()
        var objects:[ProvideMessages] = state.myElevators+state.enemyElevators
        objects.append(debug)
        for sendObject in objects
        {
          messagesToSend.append(contentsOf: sendObject.messages)
        }
        debug.messages.removeAll()
        
        var sendData = try! encoder.encode(messagesToSend)
        sendData.append("\n".data(using: .utf8)!)
        socket.write(data: sendData)
      }catch {
        if let message = try? decoder.decode([String:String].self, from: data), let text = message["message"]
        {
          print("Close with message: \(text)")
        }else{
          print("\(error)")
        }
      }
    }
  }
}


let host = ProcessInfo.processInfo.environment["WORLD_NAME"] ?? "127.0.0.1"
let solutionId = Int(ProcessInfo.processInfo.environment["SOLUTION_ID"] ?? "") ?? 0
let client = Client(host: host, port: 8000, solutionID:solutionId);
client.run()
