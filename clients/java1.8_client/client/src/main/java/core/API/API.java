package core.API;

import core.BaseStrategy;
import core.Strategy;
import javafx.util.Pair;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Created by Boris on 01.02.17.
 */

public class API {
    private Debug debug;

    private BaseStrategy strategy = null;
    public API() {
        debug = new Debug();
        try {
            strategy = new Strategy();
            strategy.setDebug(debug);
        } catch (Exception e) {
            debug.exception(e);
        }
    }
    private Pair<Pair<List<Passenger>, List<Elevator>>, Pair<List<Passenger>, List<Elevator>>> parseState(JSONObject state) {
        List<Passenger> myPassengers = new ArrayList<>();
        List<Elevator> myElevators = new ArrayList<>(3);

        for (Object passenger : (JSONArray) state.get("my_passengers")) {
            myPassengers.add(new Passenger((JSONObject) passenger));
        }

        for (Object elevator : (JSONArray) state.get("my_elevators")) {
            myElevators.add(new Elevator((JSONObject) elevator));
        }

        List<Passenger> enemyPassengers = new ArrayList<>();
        List<Elevator> enemyElevators = new ArrayList<>(3);

        for (Object passenger : (JSONArray) state.get("enemy_passengers")) {
            enemyPassengers.add(new Passenger((JSONObject) passenger));
        }

        for (Object elevator : (JSONArray) state.get("enemy_elevators")) {
            enemyElevators.add(new Elevator((JSONObject) elevator));
        }

        Pair<List<Passenger>, List<Elevator>> myPair = new Pair<>(myPassengers, myElevators);
        Pair<List<Passenger>, List<Elevator>> enemyPair = new Pair<>(enemyPassengers, enemyElevators);

        return new Pair<>(myPair, enemyPair);
    }
    public JSONArray turn(JSONObject state) {
        Pair<Pair<List<Passenger>, List<Elevator>>, Pair<List<Passenger>, List<Elevator>>> pair = parseState(state);

        try {
            this.strategy.onTick(pair.getKey().getKey(), pair.getKey().getValue(), pair.getValue().getKey(), pair.getValue().getValue());
        } catch (Exception e) {
            debug.exception(e);
        }

        JSONArray resultArray = new JSONArray();
        resultArray.addAll(Stream.of(pair.getKey().getKey().stream(),
                                     pair.getKey().getValue().stream(),
                                     pair.getValue().getKey().stream(), Stream.of(debug))
                .flatMap(Function.identity())
                .flatMap((msg)->msg.getMessages().stream()).collect(Collectors.toList()));
        return resultArray;
    }
}
