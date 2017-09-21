require.config({
    urlArgs: "bust=" + (new Date()).getTime(),
    baseUrl: "js/",
    waitSeconds: 0,
    paths: {
        'conf': 'conf',
        'init': 'init',
        'PIXI': 'libs/pixi.min',
        'game_object': 'mechanic/game_object',
        'elevator': 'mechanic/elevator',
        'passenger': 'mechanic/passenger',
        'building': 'mechanic/building',
        'events': 'events',
        'underscore': 'libs/underscore-min'
    }
});

require([
    'init',
    'utils',
    'events'
], function (init, utils, events) {
    $(document).ready(function () {
        utils.loadTextures(function () {
            events(init);
        });
    });
});