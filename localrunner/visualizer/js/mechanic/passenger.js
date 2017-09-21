define([
    'conf',
    'game_object',
    'utils'
], function (conf, GameObject, utils) {

    var PASSENGER_STATE = {
        'waiting_for_elevator': 1,
        'moving_to_elevator': 2,
        'returning': 3,
        'moving_to_floor': 4,
        'using_elevator': 5,
        'exiting': 6,
        'away': 7,
        'walking_on_floor': 8,
        'for_delete': 9
    };

    function Passenger(id, x, y, direction, state) {
        this.id = id;
        this.state = state;
        var width = conf.OPTIONS_PASSENGER.width * conf.MULTIPL;
        var height = conf.OPTIONS_PASSENGER.height * conf.MULTIPL;
        GameObject.call(this, x, y, width, height);

        this.animId = utils.randomInt(0, 2);

        this.walkSprite = this.loadFromCache(x, y, conf.OPTIONS_PASSENGER[this.animId].WALK_ANIMATION);
        this.walkSprite.visible = false;
        this.walkSprite.play();
        this.riderSprite = this.loadFromCache(x, y, conf.OPTIONS_PASSENGER[this.animId].RIDE_ANIMATION);
        this.riderSprite.visible = false;
        this.riderSprite.play();

        this.direction = direction;
        if (this.direction === 'left') {
             this.riderSprite.anchor.x = 1;
            this.walkSprite.anchor.x = 1;
            this.riderSprite.scale.x *= -1;
            this.walkSprite.scale.x *= -1;
        }
        this.state = PASSENGER_STATE['waiting_for_elevator'];
        this.elevator = null;
    }
    Passenger.prototype = Object.create(GameObject.prototype);
    Passenger.prototype.constructor = Passenger;

    Passenger.prototype.riderAnimationActivate = function () {
        this.walkSprite.visible = false;
        this.riderSprite.visible = true;
    };

    Passenger.prototype.walkAnimationActivate = function () {
        this.walkSprite.visible = true;
        this.riderSprite.visible = false;
    };

    Passenger.prototype.hideAllAnimation = function () {
        this.walkSprite.visible = false;
        this.riderSprite.visible = false;
    };

    Passenger.prototype.flip = function () {
        if (this.direction === 'left') {
            this.riderSprite.anchor.x = 0;
            this.walkSprite.anchor.x = 0;
            this.riderSprite.scale.x *= -1;
            this.walkSprite.scale.x *= -1;
            this.direction = 'right';
        } else {
            this.riderSprite.anchor.x = 1;
            this.walkSprite.anchor.x = 1;
            this.riderSprite.scale.x *= -1;
            this.walkSprite.scale.x *= -1;
            this.direction = 'left';
        }

    };

    Passenger.prototype.applyTick = function (tickData) {
        var coordinates = utils.translateCoordinates(parseFloat(tickData.x),parseFloat(tickData.y));
        this.state = tickData.state;
        coordinates.y -= conf.OPTIONS_PASSENGER.height * conf.MULTIPL;
        coordinates.x -= conf.OPTIONS_PASSENGER.width/2 * conf.MULTIPL;
        if (coordinates.x < this.x && this.direction === 'right') {
            this.flip();

        } else if (coordinates.x > this.x && this.direction === 'left') {
            this.flip();

        }
        this.x = this.walkSprite.position.x = this.riderSprite.position.x = coordinates.x;
        this.y = this.walkSprite.position.y = this.riderSprite.position.y = coordinates.y - conf.OPTIONS_FLOOR.height * conf.MULTIPL;
        if (tickData.state !== PASSENGER_STATE['waiting_for_elevator'] && tickData.state !== PASSENGER_STATE['using_elevator']) {
            this.walkAnimationActivate();
        } else if (tickData.state === PASSENGER_STATE['using_elevator']) {
            this.hideAllAnimation();
        } else {
            this.riderAnimationActivate();
        }
    };

    return Passenger;
});