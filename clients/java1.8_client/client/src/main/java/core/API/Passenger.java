package core.API;

import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Boris on 01.02.17.
 */
public class Passenger implements MessagesInterface {
    private Integer id;
    private Integer elevator;
    private Integer fromFloor;
    private Integer destFloor;
    private Integer state;
    private Integer timeToAway;
    private String type;
    private Integer floor;
    private List<JSONObject> messages;
    private Double x;
    private Double y;
    private Double weight;

    public Boolean hasElevator() {
        return this.elevator != null;
    }

    public List<JSONObject> getMessages() {
        return this.messages;
    }

    public Integer getFromFloor() {
        return this.fromFloor;
    }

    public Integer getDestFloor() {
        return this.destFloor;
    }

    public Double getY() {
        return y;
    }

    public Integer getState() {
        return state;
    }

    public Double getX() {
        return x;
    }

    public Double getWeight() {
        return weight;
    }

    public Integer getElevator() {
        return elevator;
    }

    public Integer getId() {
        return id;
    }

    public Integer getTimeToAway() { return timeToAway; }

    public String getType() { return type; }

    public Integer getFloor() { return floor; }

    public Passenger(JSONObject passenger) {
        id = (int) (long) passenger.get("id");
        elevator = passenger.get("elevator") == null ? null : (int) (long) passenger.get("elevator");
        fromFloor = (int) (long) passenger.get("from_floor");
        destFloor = (int) (long) passenger.get("dest_floor");
        timeToAway = (int) (long) passenger.get("time_to_away");
        type = (String) passenger.get("type");
        floor = (int) (long) passenger.get("floor");
        state = (int) (long) passenger.get("state");
        messages = new ArrayList<>();
        if (passenger.get("x") instanceof Long) {
            x = ((Long) passenger.get("x")).doubleValue();
        } else {
            x = (double) passenger.get("x");
        }
        if (passenger.get("y") instanceof Long) {
            y = ((Long) passenger.get("y")).doubleValue();
        } else {
            y = (double) passenger.get("y");
        }

        if (passenger.get("weight") instanceof Long) {
            weight = ((Long) passenger.get("weight")).doubleValue();
        } else {
            weight = (double) passenger.get("weight");
        }
    }
    public void setElevator(Elevator elevator) {
        this.elevator = elevator.getId();
        JSONObject jo = new JSONObject();
        jo.put("command", "set_elevator_to_passenger");
        JSONObject args = new JSONObject();
        args.put("passenger_id", this.id);
        args.put("elevator_id", elevator.getId());
        jo.put("args", args);
        this.messages.add(jo);
    }

}
