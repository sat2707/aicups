package core.API;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.*;

/**
 * Created by Boris on 01.02.17.
 */
public class Elevator implements MessagesInterface {
    private Integer id;
    private Double y;
    private List<Passenger> passengers;
    private Integer state;
    private Double speed;
    private Integer timeOnFloor;
    private Integer floor;
    private String type;
    private Integer nextFloor;
    private List<JSONObject> messages;

    public Integer getState() {
        return this.state;
    }

    public Double getSpeed() {
        return this.speed;
    }

    public Integer getNextFloor() { return this.nextFloor; }

    public Integer getTimeOnFloor() {
        return this.timeOnFloor;
    }

    public Integer getFloor() {
        return this.floor;
    }

    public String getType() {
        return this.type;
    }

    public Double getY() {
        return this.y;
    }

    public List<Passenger> getPassengers() {
        return this.passengers;
    }

    public Integer getId() {
        return this.id;
    }

    public List<JSONObject> getMessages(){
        return this.messages;
    }

    public Elevator(JSONObject elevator) {
        id = (int) (long) elevator.get("id");
        if (elevator.get("y") instanceof Long) {
            y = ((Long) elevator.get("y")).doubleValue();
        } else {
            y = (double) elevator.get("y");
        }
        passengers = new ArrayList<>();
        for (Object passenger : (JSONArray) elevator.get("passengers")) {
            passengers.add(new Passenger((JSONObject) passenger));
        }
        state = (int) (long) elevator.get("state");
        speed = (double) elevator.get("speed");
        timeOnFloor = (int) (long) elevator.get("time_on_floor");
        floor = (int) (long) elevator.get("floor");
        type = (String) elevator.get("type");
        nextFloor = (int) (long) elevator.get("next_floor");
        messages = new ArrayList<>();
    }

    public void goToFloor(Integer floor) {
        this.nextFloor = floor;
        JSONObject jo = new JSONObject();
        jo.put("command", "go_to_floor");
        JSONObject args = new JSONObject();
        args.put("elevator_id", this.id);
        args.put("floor", floor);
        jo.put("args", args);
        this.messages.add(jo);
    }
}
