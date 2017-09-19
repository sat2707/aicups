using System;
using client;
using Api;
using System.Collections.Generic;


namespace client
{
	public class strategy : baseStrategy
	{
		public override void onTick(List<Passenger> myPassengers, List<Elevator> myElevators, List<Passenger> enemyPassengers, List<Elevator> enemyElevators)
		{

			foreach (Elevator elevator in myElevators) 
			{
				foreach (Passenger passenger in myPassengers)
				{
					if (passenger.State < 5) 
					{
						if (elevator.State != 1)
						{
							elevator.GoToFloor(passenger.FromFloor);
						}

						if (elevator.Floor == passenger.FromFloor) 
						{
							passenger.SetElevator(elevator);
						}
					}
				}
				if (elevator.Passengers.Count > 0 && elevator.State != 1) 
				{
					elevator.GoToFloor(elevator.Passengers[0].DestFloor);
				}
			}
		}
	}
}
