/**
 * Created by maksimkislenko on 17.05.16.
 */

define([
    'conf',
    'building',
    'PIXI',
    'underscore'
], function (conf, Building, PIXI, _) {

    function World(data, config, renderer, scoreSetter, timeLine, console, debugInfo) {
        this.data = data;
        this.config = config;
        this.renderer = renderer;
        this.scoreAndTimeSetter = scoreSetter;
        this.timeLine = timeLine;
        this.console = console;
        this.debug = debugInfo;

        this.stage = new PIXI.Container();

        this.tilingTexture = new PIXI.extras.TilingSprite.fromFrame(window.PATH_IMG + conf.IMG.texture, renderer.width, renderer.height * 3);
        this.tilingTextureOffset = 0;
        this.tilingTextureHeight = this.tilingTexture.texture.baseTexture.source.height;
        this.stage.addChild(this.tilingTexture);

        this.building = new Building(this.config, renderer.width, renderer.height, this.stage);

        this.tickNum = 0;
        this.multiply = 1;
        this.animationId = null;
        this.tickCount = this.data.length;
        this.timerCount = ((conf.TIMER.initMinutes * 60) + conf.TIMER.initSeconds) * 1000;

        this.createTicker();
        this.animationTick();

        this.renderer.render(this.stage);

    }

    World.prototype.clearConsole = function () {
        if (this.console) {
            this.console.html('');
        }
    };

    World.prototype.createTicker = function () {
        var counterText = '';
        for (var i = 0; i < 4 - this.tickNum.toString().length; i++) {
            counterText += ' '
        }
        var fontSize = 20 * conf.MULTIPL;
        var timerSprite = new PIXI.Text('', {
            font: fontSize + 'px Monaco',
            fill: 0xffa010,
            align: 'center'
        });
        this.timerSprite = timerSprite;
        this.setTickCount(0);
        timerSprite.position.x = this.renderer.width / 2 - timerSprite.width / 2;
        timerSprite.position.y = this.renderer.height - timerSprite.height;
        this.stage.addChild(timerSprite);
    };

    World.prototype.setTickCount = function (tick) {
        var counterText = '';
        for (var i = 0; i < 4 - tick.toString().length; i++) {
            counterText += ' '
        }
        counterText += tick + '/' + this.tickCount || 0;
        this.timerSprite.text = counterText;
    };

    World.prototype.destroy = function () {
        this.tickNum = 0;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    };

    World.prototype.mechanicTick = function () {
        if (this.tickNum < 0) this.tickNum = 0;
        var tickData = this.data[this.tickNum];
        this.setTickCount(this.tickNum + 1);
        this.building.applyTick(tickData);
        this.scoreAndTimeSetter(tickData.scores, this.timerCount - (this.timerCount / this.tickCount * (this.tickNum)));
    };
    World.prototype.animationTick = function () {
        this.tilingTextureOffset += conf.BACKGROUND_ANIMATION_SPEED * this.multiply;
        this.tilingTexture.position.y -= conf.BACKGROUND_ANIMATION_SPEED * this.multiply;
        if (this.tilingTextureOffset > this.tilingTextureHeight) {
            this.tilingTexture.position.y += this.tilingTextureOffset;
            this.tilingTextureOffset = 0;
        }

        this.renderer.render(this.stage);
    };

    World.prototype.rewind = function (tick, callback) {
        if (this.debug) this.printToConsole(Math.min(20, Math.abs(this.tickNum - tick)));
        this.tickNum = tick - 1;
        this.mechanicTick();
        this.animationTick();
        if (this.data.length < this.tickNum && callback) {
            callback();
        }
    };

    World.prototype.printToConsole = function (ticksPerFrame) {

        var print = function (text, type, index) {
            if (this.console.children().length > conf.CONSOLE_VOL) {
                this.console.children().remove(':nth-child(-n+10)');
            }
            this.console.append('<br><span>Tick[' + (this.tickNum - (ticksPerFrame - index) + 1) + '] ' + type +': ' + _.escape(text) + '</span>');
            this.console[0].scrollTop = this.console[0].scrollHeight;
        }.bind(this);

        _.each(this.debug.slice(this.tickNum - ticksPerFrame, this.tickNum), function (obj, index) {
            _.each(obj, function (values, key) {
                _.each(values, function (value) {
                    print(value, key, index);
                })
            });
        })
    };


    World.prototype.show = function () {
        var self = this;
        return new Promise(function (resolve, reject) {
            var prevTickTime = 0;
            var tick = function () {
                var currentTickTime = Date.now();
                var ticksPerFrame = Math.round((currentTickTime - prevTickTime) * 0.06) * self.multiply;
                self.tickNum += ticksPerFrame;
                if (self.tickCount <= self.tickNum) {
                    self.tickNum = self.tickCount - 1;
                    self.mechanicTick();
                    self.animationTick();
                    if (self.debug) self.printToConsole(ticksPerFrame);
                    cancelAnimationFrame(self.animationId);
                    self.tickNum = 0;
                    self.animationId = undefined;
                    resolve('done');
                    return
                } else if (self.pause) {
                    cancelAnimationFrame(self.animationId);
                    self.animationId = undefined;
                    resolve('pause');
                    return
                }
                self.mechanicTick();
                self.animationTick();
                if (self.debug) self.printToConsole(ticksPerFrame);
                self.timeLine.val(self.tickNum);
                prevTickTime = currentTickTime;

                self.animationId = requestAnimationFrame(tick);
            };
            prevTickTime = Date.now();
            tick();
        });
    };
    var world = null;

    function initWorld(data, config, renderer, scoreSetter, timeLine, console, debugInfo) {
        if (world) {
            world.destroy();
        }
        world = new World(data, config, renderer, scoreSetter, timeLine, console, debugInfo);
        return world;
    }

    function destroyWorld() {
        world.destroy();
    }

    function pauseWorld() {
        if (world) {
            world.pause = true;
        }
    }

    function playWorld(callback) {
        world.pause = false;
        if (world.animationId === undefined || world.animationId === null && world) {
            world.show().then(callback);

        } else if (world && world.animationId) {
            world.pause = false;
            world.show().then(callback);
        }
    }

    function showFrom(tick, callback) {
        if (world) {
            world.rewind(tick, callback);
        }
    }

    function setMultiply(multiply) {
        if (world) {
            world.multiply = multiply
        }
    }

    return {
        'initWorld': initWorld,
        'playWorld': playWorld,
        'destroyWorld': destroyWorld,
        'pauseWorld': pauseWorld,
        'showFrom': showFrom,
        'setMultiply': setMultiply
    }
});