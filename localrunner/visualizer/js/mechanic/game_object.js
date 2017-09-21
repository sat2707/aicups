/**
 * Created by maksimkislenko on 21.06.16.
 */


define(['PIXI'], function (PIXI) {
    function GameObject(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    GameObject.prototype = Object.create({});
    GameObject.prototype.projectX = function () {
        return {start: this.x, end: this.x + this.width};
    };
    GameObject.prototype.projectY = function () {
        return {start: this.y, end: this.y + this.height};
    };

    GameObject.prototype.outWorld = function (width, height, dir) {
        var pX = this.projectX(), pY = this.projectY();
        return (dir.x == -1 && pX.start <= 0 ||
        dir.x == 1 && pX.end >= width ||
        dir.y == -1 && pY.start <= 0 ||
        dir.y == 1 && pY.end >= height);
    };
    GameObject.prototype.onTimer = function () {
    };
    GameObject.prototype._move = function (dx, dy) {
        this.x += dx;
        this.y += dy;
        this.sprite.position.x += dx;
        this.sprite.position.y += dy;
    };

    GameObject.prototype.isForDelete = function () {
        return false;
    };

    GameObject.prototype.loadFromCache = function (x, y, conf) {
        var frames = [];
        for (var i = 0; i < conf.count; i++) {
            var number;
            if (i < 10) {
                number = '0' + i;
            } else {
                number = '' + i;
            }
            frames.push(PIXI.Texture.fromFrame(window.PATH_IMG + conf.path.format(number)));
        }
        var sprite = new PIXI.extras.MovieClip(frames);
        sprite.position.x = x;
        sprite.position.y = y;
        sprite.width = this.width;
        sprite.height = this.height;
        sprite.animationSpeed = conf.speed;
        return sprite;

    };

    GameObject.prototype.loadTextureFromCache = function (x, y, conf) {
        var sprite = new PIXI.Sprite.fromFrame(window.PATH_IMG + conf.path);
        sprite.position.x = x;
        sprite.position.y = y;
        sprite.width = this.width;
        sprite.height = this.height;
        return sprite
    };

    return GameObject;
});