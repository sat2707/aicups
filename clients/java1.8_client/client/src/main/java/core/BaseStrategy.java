package core;

import core.API.Debug;
import core.API.Elevator;
import core.API.Passenger;

import java.util.List;

/**
 * Created by Boris on 01.02.17.
 */
public class BaseStrategy {
    private Debug debug;

    public void setDebug(Debug debug) {
        this.debug = debug;
    }
    public void log(Object object) {
        debug.log(object);
    }

    public void onTick(List<Passenger> myPassengers, List<Elevator> myElevators, List<Passenger> enemyPassengers, List<Elevator> enemyElevators) {
    }
}
