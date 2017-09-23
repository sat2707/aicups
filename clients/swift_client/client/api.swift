import Foundation

class Message: Encodable {
  var command:String = ""
  enum CodingKeys: String, CodingKey {
    case command
  }
}
protocol ProvideMessages {
  var messages:[Message] {get}
}

class SetElevator:Message {
  struct Arguments:Encodable {
    let passengerId: Int
    let elevatorId: Int
    enum CodingKeys: String, CodingKey {
      case passengerId = "passenger_id"
      case elevatorId = "elevator_id"
      
    }
  }
  override var command: String { get {return "set_elevator_to_passenger"}set{}}
  let args: Arguments
  
  init (elevatorId:Int, passengerId:Int)
  {
    args = Arguments(passengerId: passengerId, elevatorId: elevatorId)
  }
  
  enum AditionalCodingKeys: String, CodingKey {
    case args
  }
  
  override func encode(to encoder: Encoder) throws {
    try! super.encode(to: encoder)
    var container = encoder.container(keyedBy: AditionalCodingKeys.self)
    try! container.encode(args, forKey: .args)
  }
  
  
}

class GoToFloor:Message {
  struct Arguments:Encodable {
    let elevatorId:Int
    let floor: Int
    enum CodingKeys: String, CodingKey {
      case elevatorId = "elevator_id"
      case floor = "floor"
      
    }
  }
  override var command: String { get{return "go_to_floor"}set{}}
  let args:Arguments
  init(elevatorId:Int, floor:Int)
  {
    self.args = Arguments(elevatorId: elevatorId, floor: floor)
  }
  
  enum AditionalCodingKeys: String, CodingKey {
    case args
  }
  
  override func encode(to encoder: Encoder) throws {
    try! super.encode(to: encoder)
    var container = encoder.container(keyedBy: AditionalCodingKeys.self)
    try! container.encode(args, forKey: .args)
  }
}

class LogMessage:Message {
  struct Arguments:Encodable {
    let text:String
  }
  override var command: String { get{return "log"}set{}}
  let args:Arguments
  init(text:String)
  {
    self.args = Arguments(text:text)
  }
  
  enum AditionalCodingKeys: String, CodingKey {
    case args
  }
  
  override func encode(to encoder: Encoder) throws {
    try! super.encode(to: encoder)
    var container = encoder.container(keyedBy: AditionalCodingKeys.self)
    try! container.encode(args, forKey: .args)
  }
}

class ExceptionMessage:Message {
  struct Arguments:Encodable {
    let text:String
  }
  override var command: String { get{return "exception"}set{}}
  let args:Arguments
  init(text:String)
  {
    self.args = Arguments(text:text)
  }
  
  enum AditionalCodingKeys: String, CodingKey {
    case args
  }
  
  override func encode(to encoder: Encoder) throws {
    try! super.encode(to: encoder)
    var container = encoder.container(keyedBy: AditionalCodingKeys.self)
    try! container.encode(args, forKey: .args)
  }
}

struct FirstMessage: Codable {
  let color: String
  let message:String
}

struct WorldState:Codable {
  let myElevators:[Elevator]
  let myPassenger:[Passenger]
  let enemyElevators:[Elevator]
  let enemyPassenger:[Passenger]
  
  enum CodingKeys: String, CodingKey {
    case myElevators = "my_elevators"
    case myPassenger = "my_passengers"
    case enemyElevators = "enemy_elevators"
    case enemyPassenger = "enemy_passengers"
  }
}

class Passenger:Codable,ProvideMessages {
  enum State:Int, Codable {
    case waitingForElevator = 1,movingToElevator,returning,movingToFloor,usingElevator,exiting
  }
  
  let id:Int
  let destFloor:Int
  let weight:Float
  let fromFloor:Int
  let floor:Int
  let timeToAway:Int
  let state:State
  let x:Int
  let y:Float
  let type:String
  private(set) var elevator: Int = -1
  
  internal var messages = [Message]()
  
  init( id:Int,
        destFloor:Int,
        weight:Float,
        fromFloor:Int,
        floor:Int,
        timeToAway:Int,
        state:State,
        x:Int,
        y:Float,
        type:String) {
    self.id = id
    self.destFloor = destFloor
    self.weight = weight
    self.fromFloor = fromFloor
    self.floor = floor
    self.timeToAway = timeToAway
    self.state = state
    self.x = x
    self.y = y
    self.type = type
  }
  
  enum CodingKeys: String, CodingKey {
    case weight,state,y,floor,type,id,x
    case destFloor = "dest_floor"
    case fromFloor = "from_floor"
    case timeToAway = "time_to_away"
  }
  
  func set(elevator: Elevator) {
    self.elevator = elevator.id;
    self.messages.append(SetElevator(elevatorId: elevator.id, passengerId: self.id))
  }
  
  func hasElevator() -> Bool {
    return self.elevator != -1;
  }
  
  
}

class Elevator:Codable,ProvideMessages {
  enum State: Int,Codable{
   case waiting = 0, moving, opening, filling, closing
  }
  let passengers:[Passenger]
  let state: State
  let timeOnFloor: Int
  var nextFloor: Int
  let y:Float
  let speed: Float
  let type: String
  let id:Int
  let floor:Int
  
  internal var messages = [Message]()
  
  init(passengers:[Passenger],state:State,timeOnFloor:Int,nextFlor:Int,y:Float,speed:Float,type:String, id: Int, floor: Int) {
    self.passengers = passengers
    self.state = state
    self.timeOnFloor = timeOnFloor
    self.nextFloor = nextFlor
    self.y = y
    self.speed = speed
    self.type = type
    self.id = id
    self.floor = floor
  }
  
  enum CodingKeys: String, CodingKey {
    case passengers,state,y,speed,type,id,floor
    case timeOnFloor = "time_on_floor"
    case nextFloor = "next_floor"
  }
  
  func go(toFloor floor:Int)
  {
    self.nextFloor = floor;
    self.messages.append(GoToFloor(elevatorId: self.id, floor: floor))
  }
}

class DebugLog: Debug,ProvideMessages {
  var messages = [Message]()
  func log(object: AnyObject) {
    messages.append(LogMessage(text: object.debugDescription))
  }
  
  func `extension`(object: AnyObject) {
     messages.append(LogMessage(text: object.debugDescription))
  }
  
  
}
