<?php

require_once('base_strategy.php');
require_once('api.php');

/**
 * Main strategy class
 */
class Strategy extends BaseStrategy {

    /**
     * @inheritdoc
     */
    public function onTick(&$myPassengers, &$myElevators, &$enemyPassengers, &$enemyElevators) {
        foreach ($myElevators as $elevator) {
            foreach ($myPassengers as $passenger) {
                if ($passenger->state < 5) {
                    if ($elevator->state != 1) {
                        $elevator->goToFloor($passenger->fromFloor);
                    }
                    if ($elevator->floor == $passenger->fromFloor) {
                        $passenger->setElevator($elevator->id);
                    }
                }
                if (count($elevator->passengers) > 0 && $elevator->state != 1) {
                    $elevator->goToFloor($elevator->passengers[0]->destFloor);
                }
            }
        }
    }
}
