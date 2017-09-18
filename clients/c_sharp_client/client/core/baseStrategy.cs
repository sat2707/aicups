using System;
using Api;
using System.Collections.Generic;
namespace client
{
	public abstract class baseStrategy
	{
		private DebugClass debug;
	
		public DebugClass Debug
		{
			set { debug = value; }
		}

		public baseStrategy()
		{
		}
			
		public abstract void onTick(List<Passenger> myPassengers, List<Elevator> myElevators, List<Passenger> enemyPassengers, List<Elevator> enemyElevators);

		public void log(Object obj)
		{
			debug.log (obj);
		}
	}
}

