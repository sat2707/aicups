define(['PIXI', 'conf', 'underscore'], function (PIXI, conf, _) {
    String.prototype.format = function () {
        var i = 0, args = arguments;
        return this.replace(/{}/g, function () {
            return typeof args[i] != 'undefined' ? args[i++] : '';
        });
    };
    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    var loader = PIXI.loader;

    function loadFromConf(conf) {
        for (var i = 0; i < conf.count; i++) {
            var number;
            if (i < 10) {
                number = '0' + i;
            } else {
                number = '' + i;
            }
            loader.add(window.PATH_IMG + conf.path.format(number));
        }
    }

    function loadTextures(callback) {
        loadFromConf(conf.OPTIONS_PASSENGER[0].WALK_ANIMATION);
        loadFromConf(conf.OPTIONS_PASSENGER[0].RIDE_ANIMATION);
        loadFromConf(conf.OPTIONS_PASSENGER[1].WALK_ANIMATION);
        loadFromConf(conf.OPTIONS_PASSENGER[1].RIDE_ANIMATION);
        loadFromConf(conf.OPTIONS_PASSENGER[2].WALK_ANIMATION);
        loadFromConf(conf.OPTIONS_PASSENGER[2].RIDE_ANIMATION);


        loader.add(window.PATH_IMG + conf.OPTIONS_ELEVATOR.LIFT_OPEN_SPRITE.path);
        loader.add(window.PATH_IMG + conf.OPTIONS_ELEVATOR.LIFT_CLOSE_SPRITE.path);
        loader.add(window.PATH_IMG + conf.OPTIONS_FLOOR.path);
        loader.add(window.PATH_IMG + conf.OPTIONS_LADDER.path);
        loader.add(window.PATH_IMG + conf.OPTIONS_INDICATOR.path);
        loader.add(window.PATH_IMG + conf.IMG.texture);
        loader.load(callback);
    }

    function translateCoordinates(x, y) {
        return {
            x: ((conf.WIDTH) / 2 + x * conf.MULTIPL),
            y: ((conf.HEIGHT) - y * conf.FLOOR_HEIGHT)
        }
    }

    return {
        'randomInt': getRandomInt,
        'loadTextures': loadTextures,
        'translateCoordinates': translateCoordinates
    };
});