/**
 * Created by maksimkislenko on 21.06.16.
 */


define([
    'conf',
    'elevator',
    'passenger',
    'utils',
    'underscore',
    'PIXI'
], function (conf, Elevator, Passenger, utils, _, PIXI) {
    function Building(config, width, height, stage) {
        this.stage = stage;
        this.width = width;
        this.height = height;
        this.passengers = [];
        this.config = config;
        this.indicators = {
            'FIRST_PLAYER': {},
            'SECOND_PLAYER': {}
        };
        for (var i = 0; i < config.FLOORS_COUNT; i++) {
            this.renderFloor(i + 1);
        }
        this.elevators = [];

        this.passengerIndicators = new PIXI.Container();
        this.passengerIndicators.width = 1000;
        this.passengerIndicators.height = 1000;

        for (var i = 0; i < config.ELEVATORS_FOR_PASSENGER_COUNT; i++) {
            var mechanicPositionX = config.FIRST_ELEVATOR_POSITION - conf.OPTIONS_ELEVATOR.width / 2 + i * config.ELEVATOR_IN_GROUP_OFFSET;
            var mechanicPositionY = 1;
            var leftElevatorPosition = utils.translateCoordinates(-mechanicPositionX, mechanicPositionY);
            var rightElevatorPosition = utils.translateCoordinates(mechanicPositionX, mechanicPositionY);

            this.elevators.unshift(new Elevator(
                leftElevatorPosition.x - conf.OPTIONS_ELEVATOR.width * conf.MULTIPL,
                leftElevatorPosition.y - conf.OPTIONS_ELEVATOR.height * conf.MULTIPL
            ));

            this.elevators.push(new Elevator(
                rightElevatorPosition.x,
                rightElevatorPosition.y - conf.OPTIONS_ELEVATOR.height * conf.MULTIPL
            ));

        }

        this.objects = this.elevators.slice();
        this.objects.forEach(function (elevator) {
            this.stage.addChild(elevator.openSprite);
            this.stage.addChild(elevator.closeSprite);
        }, this);
        this.stage.addChild(this.passengerIndicators);

    }

    Building.prototype.renderFloor = function (floor) {
        var centerFloor = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_FLOOR.path);
        var mechanicPositionX = -this.config.FIRST_ELEVATOR_POSITION + conf.OPTIONS_ELEVATOR.width / 2;
        var mechanicPositionY = floor;
        var leftSpritePosition = null;
        var rightSpritePosition = null;
        var spriteWidth = (2 * this.config.FIRST_ELEVATOR_POSITION - conf.OPTIONS_ELEVATOR.width) * conf.MULTIPL;
        var spritePosition = utils.translateCoordinates(mechanicPositionX, mechanicPositionY);
        centerFloor.position.x = spritePosition.x;
        centerFloor.position.y = spritePosition.y - conf.OPTIONS_FLOOR.height * conf.MULTIPL;

        centerFloor.width = spriteWidth;
        centerFloor.height = conf.OPTIONS_FLOOR.height * conf.MULTIPL;

        this.stage.addChild(centerFloor);

        for (var i = 0; i < this.config.ELEVATORS_FOR_PASSENGER_COUNT; i++) {
            mechanicPositionX = this.config.FIRST_ELEVATOR_POSITION + conf.OPTIONS_ELEVATOR.width / 2 + i * (this.config.ELEVATOR_IN_GROUP_OFFSET);
            if (this.config.ELEVATORS_FOR_PASSENGER_COUNT - i === 1) {
                spriteWidth = this.config.INDICATOR_POSITION - conf.OPTIONS_INDICATOR.width / 2 - (this.config.FIRST_ELEVATOR_POSITION + conf.OPTIONS_ELEVATOR.width / 2 + i * (this.config.ELEVATOR_IN_GROUP_OFFSET));
            } else {
                spriteWidth = this.config.ELEVATOR_IN_GROUP_OFFSET - conf.OPTIONS_ELEVATOR.width;
            }
            spriteWidth *= conf.MULTIPL;

            leftSpritePosition = utils.translateCoordinates(-mechanicPositionX, mechanicPositionY);
            rightSpritePosition = utils.translateCoordinates(mechanicPositionX, mechanicPositionY);

            var leftFloorSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_FLOOR.path);
            var rightFloorSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_FLOOR.path);

            leftFloorSprite.position.x = leftSpritePosition.x - spriteWidth;
            rightFloorSprite.position.x = rightSpritePosition.x;

            leftFloorSprite.position.y = leftSpritePosition.y - conf.OPTIONS_FLOOR.height * conf.MULTIPL;
            rightFloorSprite.position.y = rightSpritePosition.y - conf.OPTIONS_FLOOR.height * conf.MULTIPL;

            leftFloorSprite.width = spriteWidth;
            rightFloorSprite.width = spriteWidth;

            leftFloorSprite.height = conf.OPTIONS_FLOOR.height * conf.MULTIPL;
            rightFloorSprite.height = conf.OPTIONS_FLOOR.height * conf.MULTIPL;

            this.stage.addChild(leftFloorSprite, rightFloorSprite);

        }

        mechanicPositionX = this.config.INDICATOR_POSITION - conf.OPTIONS_INDICATOR.width / 2;
        leftSpritePosition = utils.translateCoordinates(-mechanicPositionX, mechanicPositionY);
        rightSpritePosition = utils.translateCoordinates(mechanicPositionX, mechanicPositionY);

        var leftIndicatorSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_INDICATOR.path);
        var rightIndicatorSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_INDICATOR.path);

        var leftIndicatorText = new PIXI.Text(0, {
            font: 30 + 'px Monaco',
            fill: 0xffffff,
            align: 'center'
        });

        var rightIndicatorText = new PIXI.Text(0, {
            font: 30 + 'px Monaco',
            fill: 0xffffff,
            align: 'center'
        });


        leftIndicatorSprite.position.x = leftSpritePosition.x - conf.OPTIONS_INDICATOR.width * conf.MULTIPL;
        rightIndicatorSprite.position.x = rightSpritePosition.x;

        leftIndicatorSprite.position.y = leftSpritePosition.y - conf.OPTIONS_INDICATOR.height * conf.MULTIPL;
        rightIndicatorSprite.position.y = rightSpritePosition.y - conf.OPTIONS_INDICATOR.height * conf.MULTIPL;

        leftIndicatorSprite.width = conf.OPTIONS_INDICATOR.width * conf.MULTIPL;
        rightIndicatorSprite.width = conf.OPTIONS_INDICATOR.width * conf.MULTIPL;

        leftIndicatorSprite.height = conf.OPTIONS_INDICATOR.height * conf.MULTIPL;
        rightIndicatorSprite.height = conf.OPTIONS_INDICATOR.height * conf.MULTIPL;

        var leftBounds = leftIndicatorSprite.getBounds();
        leftIndicatorText.position.x = (leftBounds.width - leftIndicatorText.width) / 2;
        leftIndicatorText.position.y = (leftBounds.height - leftIndicatorText.height) / 2;


        var rightBounds = rightIndicatorSprite.getBounds();
        rightIndicatorText.position.x = (rightBounds.width - rightIndicatorText.width) / 2;
        rightIndicatorText.position.y = (rightBounds.height - rightIndicatorText.height) / 2;

        leftIndicatorSprite.addChild(leftIndicatorText);
        rightIndicatorSprite.addChild(rightIndicatorText);

        this.indicators['FIRST_PLAYER'][floor.toString()] = leftIndicatorText;
        this.indicators['SECOND_PLAYER'][floor.toString()] = rightIndicatorText;
        this.stage.addChild(leftIndicatorSprite, rightIndicatorSprite);


        mechanicPositionX = this.config.LADDER_POSITION - conf.OPTIONS_LADDER.width / 2;
        leftSpritePosition = utils.translateCoordinates(-mechanicPositionX, mechanicPositionY);
        rightSpritePosition = utils.translateCoordinates(mechanicPositionX, mechanicPositionY);

        var leftLadderSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_LADDER.path);
        var rightLadderSprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.OPTIONS_LADDER.path);

        leftLadderSprite.x = leftSpritePosition.x - conf.OPTIONS_LADDER.width * conf.MULTIPL;
        rightLadderSprite.x = rightSpritePosition.x;

        leftLadderSprite.y = leftSpritePosition.y - conf.OPTIONS_LADDER.height * conf.MULTIPL;
        rightLadderSprite.y = rightSpritePosition.y - conf.OPTIONS_LADDER.height * conf.MULTIPL;

        leftLadderSprite.width = conf.OPTIONS_LADDER.width * conf.MULTIPL;
        rightLadderSprite.width = conf.OPTIONS_LADDER.width * conf.MULTIPL;

        leftLadderSprite.height = conf.OPTIONS_LADDER.height * conf.MULTIPL;
        rightLadderSprite.height = conf.OPTIONS_LADDER.height * conf.MULTIPL;

        this.stage.addChild(leftLadderSprite, rightLadderSprite);

    };
    Building.prototype.applyTick = function (tickData) {
        _.each(this.indicators, function (indicators, player) {
            _.each(indicators, function (sprite, indicator) {
                sprite.text = tickData.waiting_passengers[player][indicator] || 0;
            });
        });

        _.each(this.elevators, function (elevator, index) {
            if (index > tickData.elevators.length) return;
            elevator.applyTick(tickData.elevators[index]);
        });

        var tickPassengers = tickData.passengers.slice();
        var groups = {};
        this.passengers.forEach(function (passenger) {
            var passengerIndex = tickPassengers.findIndex(function (element) {
                return element.id === passenger.id;
            });
            if (passengerIndex === -1) {
                passengerIndex = this.passengers.indexOf(passenger);
                this.stage.removeChild(passenger.riderSprite);
                this.stage.removeChild(passenger.walkSprite);
                this.passengers.splice(passengerIndex, 1);
            } else {
                passenger.applyTick(tickPassengers[passengerIndex]);
                groups[[passenger.x, passenger.y, passenger.state]] = 1 + (groups[[passenger.x, passenger.y, passenger.state]] || 0);
                tickPassengers.splice(passengerIndex, 1);
            }
        }, this);

        tickPassengers.forEach(function (newPassenger) {
            var direction = "right";
            if (newPassenger.type === "FIRST_PLAYER") direction = "left";
            var coordinates = utils.translateCoordinates(parseFloat(newPassenger.x), parseFloat(newPassenger.y));
            var passenger = new Passenger(newPassenger.id,
                coordinates.x - conf.OPTIONS_PASSENGER.width / 2 * conf.MULTIPL,
                coordinates.y,
                direction,
                newPassenger.state
            );
            this.passengers.push(passenger);
            groups[[passenger.x, passenger.y, passenger.state]] = 1 + (groups[[passenger.x, passenger.y, passenger.state]] || 0);
            this.stage.addChild(passenger.riderSprite);
            this.stage.addChild(passenger.walkSprite);
        }, this);

        this.passengerIndicators.removeChildren();
        _.each(groups, function (value, key) {
            if (value > 1) {
                var passengerIndicator = new PIXI.Text(value, {
                    font: 15 + 'px Monaco',
                    fill: 0x000000,
                    align: 'center'
                });
                var xy = key.split(',');
                if (xy[0] < (conf.WIDTH - conf.OPTIONS_PASSENGER.width * conf.MULTIPL) / 2) {
                    xy[0] = Number(xy[0]) - passengerIndicator.width;
                } else {
                    xy[0] = Number(xy[0]) + conf.OPTIONS_PASSENGER.width * conf.MULTIPL;
                }
                passengerIndicator.position.x = xy[0];
                passengerIndicator.position.y = xy[1];
                this.passengerIndicators.addChild(passengerIndicator);
            }
        }, this);
    };
    return Building;
});