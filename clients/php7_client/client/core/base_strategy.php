<?php
abstract class BaseStrategy {
     /**
     * @var Debug
     */
    private $debug;

    function __construct($debug) {
        $this->debug = $debug;
    }

    /**
     * @param string $message
     */
    function log($message) {
        $this->debug->log($message);
    }

    function on_tick($my_passengers, $my_elevators, $enemy_passengers, $enemy_elevators) {
        return;
    }
}