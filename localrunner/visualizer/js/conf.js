/**
 * Created by maksimkislenko on 17.05.16.
 */

define([], function () {
    return {
        MULTIPL: 1,
        FLOOR_HEIGHT: 63,
        BACKGROUND_ANIMATION_SPEED: 1,
        OPTIONS_ELEVATOR: {
            width: 45,
            height: 62,
            LIFT_OPEN_SPRITE: {
                path: '1/elevator/lift04.png'
            },
            LIFT_CLOSE_SPRITE: {
                path: '1/elevator/lift00.png'
            },
            LIFT_ANIMATION: {
                path: '1/elevator/lift{}.png',
                count: 5,
                speed: 0.2,
            }
        },
        OPTIONS_LADDER: {
            width: 50,
            height: 63,
            path: '1/ladder.png'
        },
        OPTIONS_FLOOR: {
            // width: ,
            height: 7,
            path: '1/floor.png'
        },
        OPTIONS_INDICATOR: {
            width: 30,
            height: 63,
            path: '1/indicator.png'
        },
        OPTIONS_PASSENGER: {
            width: 45,
            height: 45,
            0: {
                WALK_ANIMATION: {
                    path: '1/passengers/0/walk/pers-{}.png',
                    count: 8,
                    speed: 0.3
                },
                RIDE_ANIMATION: {
                    path: '1/passengers/0/rider/pers-{}.png',
                    count: 6,
                    speed: 0.1
                }
            },
            1: {
                WALK_ANIMATION: {
                    path: '1/passengers/1/walk/pers-{}.png',
                    count: 8,
                    speed: 0.3
                },
                RIDE_ANIMATION: {
                    path: '1/passengers/1/rider/pers-{}.png',
                    count: 6,
                    speed: 0.1
                }
            },
            2: {
               WALK_ANIMATION: {
                    path: '1/passengers/2/walk/pers-{}.png',
                    count: 8,
                    speed: 0.3
                },
                RIDE_ANIMATION: {
                    path: '1/passengers/2/rider/pers-{}.png',
                    count: 6,
                    speed: 0.1
                }
            },
            floorXShift: -5,
            floorYShift: -5
        },
        IMG: {
            texture: '1/pattern.png',
            floor: '1/floor.png'
        },
        TIMER: {
            initMinutes: 2,
            initSeconds: 0
        },
        CONSOLE_VOL: 200
    };
});