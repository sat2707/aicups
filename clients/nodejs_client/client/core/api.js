class Elevator {
    constructor({id, y, passengers, state, speed, floor, next_floor, time_on_floor, type}) {
        this.id = id;
        this._y = y;
        this._passengers = passengers.map((passenger) => {
            return new Passenger(passenger);
        });
        this._state = state;
        this._speed = speed;
        this._floor = floor;
        this._nextFloor = next_floor;
        this._timeOnFloor = time_on_floor;
        this._type = type;
        this._messages = [];
    }

    get messages() {
        return this._messages;
    }

    get y() {
        return this._y;
    }

    get passengers() {
        return this._passengers
    }

    get speed() {
        return this._speed;
    }

    get floor() {
       return this._floor;
    }

    get nextFloor() {
        return this._nextFloor;
    }

    get timeOnFloor() {
        return this._timeOnFloor;
    }
    get state() {
        return this._state;
    }

    get type() {
        return this._type;
    }

    get floors() {
        return this._floors;
    }

    goToFloor(floor) {
        this._nextFloor = floor;
        this._messages.push({
            'command': 'go_to_floor',
            'args': {
                'elevator_id': this.id,
                'floor': floor
            }
        })
    }
}

class Passenger {
    constructor({id, elevator, x, y, state, time_to_away, from_floor, dest_floor, type, floor, weight}) {
        this.id = id;
        this._elevator = elevator;
        this._fromFloor = from_floor;
        this._destFloor = dest_floor;
        this._timeToAway = time_to_away;
        this._state = state;
        this._floor = floor;
        this._type = type;
        this._messages = [];
        this._x = x;
        this._y = y;
        this._weight = weight
    }

    get weight() {
        return this._weight;
    }

    get elevator() {
        return this._elevator;
    }

    get fromFloor() {
        return this._fromFloor;
    }

    get destFloor() {
        return this._destFloor;
    }

    get state() {
        return this._state;
    }

    get timeToAway() {
        return this._timeToAway;
    }

    get floor() {
        return this._floor;
    }

    get type() {
        return this._type;
    }

    get x() {
        return this._x;
    }

    get y() {
        return this._y;
    }

    get messages() {
        return this._messages;
    }

    setElevator(elevator) {
        this._elevator = elevator;
        this._messages.push({
            'command': 'set_elevator_to_passenger',
            'args': {
                'elevator_id': elevator.id,
                'passenger_id': this.id
            }
        });
    }

    hasElevator() {
        return this._elevator !== undefined && this._elevator !== null;
    }


}

class Debug {
    constructor() {
        this._messages = [];
    }

    get messages() {
        let msg = this._messages;
        this._messages = [];
        return msg
    }

    log(text) {
        this._messages.push({
            'command': 'log',
            'args': {
                'text': String(text)
            }
        })
    }

    exception(text) {
        this._messages.push({
            'command': 'exception',
            'args': {
                'text': String(text)
            }
        })
    }
}

class API {

    constructor() {
        try {
            this.debug = new Debug();
            let Strategy = require('./strategy').Strategy;
            this.strategy = new Strategy(this.debug);
        }
        catch (err) {
            this.debug.exception(err);
        }
    }
    parseState(state) {
        let my_passengers = state['my_passengers'];
        let my_elevators = state['my_elevators'];

        let enemy_passengers = state['enemy_passengers'];
        let enemy_elevators = state['enemy_elevators'];

        my_passengers = my_passengers.map((passenger) => {
            return new Passenger(passenger);
        });
        my_elevators = my_elevators.map((elevator) => {
           return new Elevator(elevator)
        });

        enemy_passengers = enemy_passengers.map((passenger) => {
            return new Passenger(passenger);
        });
        enemy_elevators = enemy_elevators.map((elevator) => {
           return new Elevator(elevator)
        });

        return [my_passengers, my_elevators, enemy_passengers, enemy_elevators]
    }

    turn(state) {
        let states = this.parseState(state);
        let my_passengers = states[0];
        let my_elevators = states[1];
        let enemy_passengers = states[2];
        let enemy_elevators = states[3];
        // console.log(my_passengers, my_elevators, enemy_passengers, enemy_elevators);
//
        try {
            this.strategy.onTick(my_passengers, my_elevators, enemy_passengers, enemy_elevators);
        }
        catch (err) {
            this.debug.exception(err);
        }
        return [].concat.apply([],
            my_elevators.map((elevator) => {return elevator.messages})
                .concat(my_passengers.map((passenger) => {return passenger.messages}))
                .concat(enemy_passengers.map(passenger => {return passenger.messages }))
                .concat(this.debug.messages));

    }
}
module.exports.API = API;
