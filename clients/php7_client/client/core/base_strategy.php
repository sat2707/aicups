<?php
    class BaseStrategy {
        
        protected $debug;
                
        function __construct($debug) {
            $this->debug = $debug;
        }
        
        protected function log($text) {
            $this->debug->log($text);
        }
        
        function on_tick($my_passengers, $my_elevators, $enemy_passengers, $enemy_elevators) {
            return;
        }
    }
?>
