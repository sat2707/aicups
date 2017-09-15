let BaseStrategy = require('./basestrategy').BaseStrategy;

class Strategy extends BaseStrategy {
    onTick(myPassengers, myElevators, enemyPassengers, enemyElevators) {
        myElevators.forEach(elevator => {
            myPassengers.forEach(passenger => {
                if (elevator.state != 1) {
                    elevator.goToFloor(passenger.fromFloor);
                }
                if (elevator.floor == passenger.fromFloor) {
                    passenger.setElevator(elevator);
                }
            })
            if (elevator.passengers.length > 0 && elevator.state != 1) {
                elevator.goToFloor(elevator.passengers[0].destFloor)
            }
        });
    }
}

module.exports.Strategy = Strategy;
