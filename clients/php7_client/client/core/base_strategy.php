<?php

/**
 * Base strategy class
 */
class BaseStrategy
{

    /**
     * Debugger object
     * @var Debug 
     */
    protected $_debug;

    /**
     * 
     * @param Debug $debug
     */
    function __construct($debug)
    {
        $this->_debug = $debug;
    }

    /**
     * Push log message
     * @param string $text
     */
    protected function log($text)
    {
        $this->debug->log($text);
    }
    
    /**
     * Called every tick
     * @param Passenger[] $myPassengers
     * @param Elevator[] $myElevators
     * @param Passenger[] $enemyPassengers
     * @param Elevator[] $enemyElevators
     */
    function onTick(&$myPassengers, &$myElevators, &$enemyPassengers, &$enemyElevators)
    {
        return;
    }
}
