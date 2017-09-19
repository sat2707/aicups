<?php

require('base_strategy.php');

class Strategy extends BaseStrategy
{

    /**
     * Process strategy turn
     * @param Passenger[] $myPassengers
     * @param Elevator[] $myElevators
     * @param Passenger[] $enemyPassengers
     * @param Elevator[] $enemyElevators
     */
    public function onTick(&$myPassengers, &$myElevators, &$enemyPassengers, &$enemyElevators)
    {
        foreach ($myElevators as $elevator) {
            foreach ($myPassengers as $passenger) {
                if ($passenger->state < 5) {
                    if ($elevator->state != 1) {
                        $elevator->goToFloor($passenger->fromFloor);
                    }
                    if ($elevator->floor == $passenger->fromFloor) {
                        $passenger->setElevator($elevator);
                    }
                }
                if (count($elevator->passengers) > 0 && $elevator->state != 1) {
                    $elevator->goToFloor($elevator->passengers[0]->destFloor);
                }
            }
        }
    }

}
