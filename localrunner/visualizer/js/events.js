define(['conf', 'underscore'], function (conf, _) {
    function scoreAndTimeSetter(element, users) {
        var scoreHtmlFirst = element.find('.js-current-score-first-player');
        var scoreHtmlSecond = element.find('.js-current-score-second-player');

        var timeHtml = element.find('.js-till-time');
        return function setScoreAndTime(scores, milliseconds) {
            var seconds = Math.floor(milliseconds / 1000) % 60;
            var minutes = Math.floor(Math.floor(milliseconds / 1000) / 60);
            var time = ((minutes < 10) ? '0' : '') + minutes + ((seconds < 10) ? ':0' : ':') + seconds;
            scoreHtmlFirst.html(scores.FIRST_PLAYER);
            scoreHtmlSecond.html(scores.SECOND_PLAYER);
            timeHtml.html(time);
        }
    }

    function registerEvents(init) {
        var runButton = $('.js-run');
        var pauseButton = $('.js-pause');
        var x1Button = $('.js-x1');
        var x2Button = $('.js-x2');
        var x4Button = $('.js-x4');
        var range = $('.range');
        var currentSpan = $('.js-score-time-user');
        var leftConsole = $('#left-console');
        var rightConsole = $('#right-console');

        var visio = data;
        var config = visio.config;
        var ww = $('#world-wrap');

        conf.MULTIPL = (ww.width() / (config.LADDER_POSITION * 2 + conf.OPTIONS_LADDER.width));
        conf.WIDTH = ww.width();
        conf.FLOOR_HEIGHT *= conf.MULTIPL;
        conf.HEIGHT = (config.FLOORS_COUNT + 1) * conf.FLOOR_HEIGHT;

        var renderer = new PIXI.autoDetectRenderer(conf.WIDTH, conf.HEIGHT);
        var world = init.initWorld(visio.game_data, config, renderer, scoreAndTimeSetter(currentSpan, visio.players), range, leftConsole, rightConsole);

        range.val(0);
        range.prop("disabled", false);
        range.removeClass('btn_disabled');

        ww.html(renderer.view);
        leftConsole.height(ww.height());
        rightConsole.height(ww.height());
        $('.preloader').fadeOut();


        x1Button.click(function () {
            init.setMultiply(1);
            $('.pressed').removeClass('pressed');
            $(this).addClass('pressed')
        });
        x2Button.click(function () {
            init.setMultiply(2);
            $('.pressed').removeClass('pressed');
            $(this).addClass('pressed')

        });
        x4Button.click(function () {
            init.setMultiply(4);
            $('.pressed').removeClass('pressed');
            $(this).addClass('pressed')
        });

        runButton.click(function () {
            if ($(this).hasClass('btn_disabled')) return;
            init.playWorld(function () {
                pauseButton.click();
            });
            pauseButton.removeClass('btn_disabled');
            $(this).addClass('btn_disabled');
        });
        pauseButton.click(function () {
            if ($(this).hasClass('btn_disabled'))
                return;
            init.pauseWorld();
            $(this).addClass('btn_disabled');
            runButton.removeClass('btn_disabled');
        });

        range.on('input', function () {
            init.showFrom($(this).val(), function () {
                pauseButton.addClass('btn_disabled');
                runButton.removeClass('btn_disabled');
            });
        });
    }

    return registerEvents;
});