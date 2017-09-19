using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using client;
using System.Text;


namespace Api
{
	public class Elevator
	{
		private int id;
		private float y;
		private List<Passenger> passengers;
		private int state;
		private float speed;
		private int timeOnFloor;
		private int nextFloor;
		private int floor;
		private String type;
		private List<JObject> messages;

		public int Id
		{
			get { return id; }
		}
		public float Y
		{
			get { return y; }

		}
		public List<Passenger> Passengers
		{
			get { return passengers; }

		}
		public int State
		{
			get { return state; }

		}
		public float Speed
		{ 
			get { return speed; }
		}
        public String Type
		{
			get { return type; }
		}

		public int TimeOnFloor
		{
			get { return timeOnFloor; }

		}

		public int NextFloor
		{
			get { return nextFloor; }
		}

		public int Floor 
		{ 
			get { return floor; }
		}


		public List<JObject> Messages
		{
			get { return messages; }

		}
			
		public Elevator (JObject elevator)
		{
			
			this.id = (int)elevator.GetValue("id");
			this.y = (float)elevator.GetValue("y");

			this.passengers = new List<Passenger>();
			foreach (Object passennger in (JArray)elevator.GetValue("passengers"))
			{
				passengers.Add(new Passenger((JObject)passennger));
			}

			this.state = (int)elevator.GetValue("state");
			this.speed = (float)elevator.GetValue("speed");
			this.timeOnFloor = (int)elevator.GetValue("time_on_floor");
			this.nextFloor = (int)elevator.GetValue("next_floor");
			this.floor = (int)elevator.GetValue("floor");
			this.type = (String)elevator.GetValue("type");

			this.messages = new List<JObject> ();
		}

		public void GoToFloor (int floor)
		{
			this.nextFloor = floor;
			JObject message = new JObject ();
			message["command"] = "go_to_floor";
			JObject args = new JObject ();
			args["elevator_id"] = this.id;
			args ["floor"] = floor;
			message["args"] = args;
			this.messages.Add (message);
		}

	}

	public class Passenger
	{
		private int id;
		private int elevator;
		private float x;
		private float y;
		private int from_floor;
		private int dest_floor;
		private int state;
		private int timeToAway;
		private float weight;
		private String type;
		private int floor;
		private List<JObject> messages;

		public int Id
		{
			get { return id; }
		}

		public int Elevator
		{ 
			get { return elevator; }
		}

		public float X
		{
			get { return x; }

		}
		public float Weight
		{
			get { return weight; }

		}

		public float Y
		{
			get { return y; }

		}

		public int FromFloor
		{
			get { return from_floor; }

		}
		public int DestFloor
		{
			get { return dest_floor; }

		}
		public int State
		{
			get { return state; }

		}

		public int TimeToAway
		{ 
			get { return timeToAway; }
		}

		public String Type 
		{ 
			get { return type; }
		}

		public int Floor 
		{
			get { return floor; }
		} 

		public List<JObject> Messages
		{
			get { return messages; }

		}


		public Passenger (JObject passenger)
		{
			id = (int)passenger.GetValue ("id");
			try {
				elevator = (int)passenger.GetValue ("elevator");
			}
			catch (System.ArgumentException) {
				elevator = -1;
			}
			x = (float)passenger.GetValue("x");
			y = (float)passenger.GetValue("y");
			weight = (float)passenger.GetValue("weight");

			from_floor = (int)passenger.GetValue ("from_floor");
			dest_floor = (int)passenger.GetValue ("dest_floor");
			state =  (int)passenger.GetValue ("state");

			timeToAway = (int)passenger.GetValue("time_to_away");
			type = (String)passenger.GetValue("type");
			floor = (int)passenger.GetValue("floor");

			messages = new List<JObject>();
		}

		public void SetElevator (Elevator elevator)
		{
			this.elevator = elevator.Id;

			JObject message = new JObject ();
			message["command"] = "set_elevator_to_passenger";
			JObject args = new JObject ();
			args["passenger_id"] = this.id;
			args ["elevator_id"] = elevator.Id;
			message["args"] = args;

			this.messages.Add (message);
		}

		public bool HasElevator ()
		{
			return (this.elevator != -1);
		}


	}

	public class DebugClass
	{
		List<JObject> messages;

		public DebugClass()
		{
			messages = new List<JObject>();
		}

		public List<JObject> Messages
		{
			get 
			{
				List<JObject> messages = this.messages;
				this.messages = new List<JObject>();
				return messages;
			}
		}

		public void log(Object obj)
		{
			JObject message = new JObject ();
			message["command"] = "log";
			JObject args = new JObject ();
			args["text"] = obj.ToString();
			message["args"] = args;

			this.messages.Add (message);
		}

		public void exception(Object obj)
		{
			JObject message = new JObject ();
			message["command"] = "exception";
			JObject args = new JObject ();
			args["text"] = obj.ToString();
			message["args"] = args;

			this.messages.Add (message);
		}

	}

	public class api
	{
		DebugClass debug;
		baseStrategy strategy = null;


		public api() 
		{
			debug = new DebugClass ();
			try 
			{
				strategy = new client.strategy ();
				strategy.Debug = debug;
			} catch (Exception e)
			{
				debug.exception (e);
			}
		}

		private Tuple<List<Passenger>, List<Elevator>, List<Passenger>, List<Elevator>> parseState (JObject state)
		{
			List<Passenger> myPassengers = new List<Passenger>();
			List<Elevator> myElevators = new List<Elevator>(3);

			foreach (Object passennger in (JArray) state.GetValue("my_passengers")) {
				myPassengers.Add (new Passenger ((JObject)passennger));
			}
			foreach (Object elevator in (JArray) state.GetValue("my_elevators")) {
				myElevators.Add (new Elevator ((JObject)elevator));
			}

			List<Passenger> enemyPassengers = new List<Passenger>();
			List<Elevator> enemyElevators = new List<Elevator>(3);

			foreach (Object passennger in (JArray)state.GetValue("enemy_passengers"))
			{
				enemyPassengers.Add(new Passenger((JObject)passennger));
			}
			foreach (Object elevator in (JArray)state.GetValue("enemy_elevators"))
			{
				enemyElevators.Add(new Elevator((JObject)elevator));
			}


			return new Tuple<List<Passenger>, List<Elevator>, List<Passenger>, List<Elevator>>(myPassengers, myElevators, enemyPassengers, enemyElevators);
		}

		public JArray turn (JObject state) {
			Tuple<List<Passenger>, List<Elevator>, List<Passenger>, List<Elevator>> quadruple = parseState(state);
			try 
			{
				this.strategy.onTick (quadruple.Item1, quadruple.Item2, quadruple.Item3, quadruple.Item4);
			} catch (Exception e) 
			{
				debug.exception (e);
			}

			JArray resultArray = new JArray ();

			foreach (Passenger passenger in quadruple.Item1) {
				foreach(JObject jo in passenger.Messages) resultArray.Add(jo);
			}

			foreach (Elevator elevator in quadruple.Item2) {
				foreach(JObject jo in elevator.Messages) resultArray.Add(jo);
			}

			foreach (Passenger passenger in quadruple.Item3)
			{
				foreach (JObject jo in passenger.Messages) resultArray.Add(jo);
			}

			foreach(JObject jo in debug.Messages) { resultArray.Add (jo); Console.WriteLine (jo); };

			return resultArray;
		}

	}
}

