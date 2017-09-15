<?php
    class BaseStrategy {
        function __construct($debug) {
            $this->debug = $debug->log;
        }

        function on_tick($my_passengers, $my_elevators, $enemy_passengers, $enemy_elevators) {
            return;
        }
    }
?>
