class BaseStrategy {
    constructor(debug) {
        this.debug = debug.log.bind(debug);
    }

    onTick(myPassengers, myElevators, enemyPassengers, enemyElevators) {

    }
}
module.exports.BaseStrategy = BaseStrategy;
