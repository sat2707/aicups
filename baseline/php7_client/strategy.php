<?php

require('base_strategy.php');

class Strategy extends BaseStrategy
{

    public function onTick(&$my_passengers, &$my_elevators, &$enemy_passengers, &$enemy_elevators)
    {
        foreach ($my_elevators as $elevator) {
            foreach ($my_passengers as $passenger) {
                if ($passenger->state < 5) {
                    if ($elevator->state != 1) {
                        $elevator->goToFloor($passenger->from_floor);
                    }
                    if ($elevator->floor == $passenger->from_floor) {
                        $passenger->setElevator($elevator);
                    }
                }
                if (count($elevator->passengers) > 0 && $elevator->state != 1) {
                    $elevator->goToFloor($elevator->passengers[0]->dest_floor);
                }
            }
        }
    }

}
