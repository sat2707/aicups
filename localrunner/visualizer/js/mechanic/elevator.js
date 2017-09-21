/**
 * Created by maksimkislenko on 21.06.16.
 */


define([
    'conf',
    'game_object',
    'utils'
], function (conf, GameObject, utils) {

    var ELEVATOR_STATE = {
        'waiting': 0,
        'moving': 1,
        'opening': 2,
        'filling': 3,
        'closing': 4
    };

    function Elevator(x, y, floor, _) {
        this.width = conf.OPTIONS_ELEVATOR.width * conf.MULTIPL;
        this.height = conf.OPTIONS_ELEVATOR.height * conf.MULTIPL;
        GameObject.call(this, x, y, this.width, this.height);

        this.openSprite = this.loadTextureFromCache(x, y, conf.OPTIONS_ELEVATOR.LIFT_OPEN_SPRITE);
        this.closeSprite = this.loadTextureFromCache(x, y, conf.OPTIONS_ELEVATOR.LIFT_CLOSE_SPRITE);

        this.isOpen = true;
        this.openSprite.visible = true;
        this.closeSprite.visible = false;

        this.state = ELEVATOR_STATE['filling'];
    }

    Elevator.prototype = Object.create(GameObject.prototype);
    Elevator.prototype.constructor = Elevator;

    Elevator.prototype.open = function () {
        this.isOpen = true;
        this.openSprite.visible = true;
        this.closeSprite.visible = false;
    };

    Elevator.prototype.close = function () {
        this.isOpen = false;
        this.openSprite.visible = false;
        this.closeSprite.visible = true;
    };

    Elevator.prototype.applyTick = function (elevData) {
        var coordinates = utils.translateCoordinates(0, parseFloat(elevData.y));

        this.openSprite.position.y = coordinates.y - conf.OPTIONS_ELEVATOR.height * conf.MULTIPL;
        this.closeSprite.position.y = coordinates.y - conf.OPTIONS_ELEVATOR.height * conf.MULTIPL;

        if (!this.isOpen && (elevData.state === ELEVATOR_STATE['filling'])) {
            this.open();
        }
        if (this.isOpen && (elevData.state === ELEVATOR_STATE['closing'])) {
            this.close();
        }

    };

    return Elevator;
});