<?php

/**
 * Elevator (read-only)
 */
class Elevator
{
    
    /**
     * Elevator waiting between closing and moving
     */
    const STATE_WAITING = 0;
    
    /**
     * Elevator moving to destignated floor
     */
    const STATE_MOVING = 1;
    
    /**
     * Elevator opening the doors
     */
    const STATE_OPENING = 2;
    
    /**
     * Elevator ready to filling passengers
     */
    const STATE_FILLING = 3;
    
    /**
     * Elevator closing the doors
     */
    const STATE_CLOSING = 4;

    /**
     * Elevator identifier
     * @var integer
     */
    public $id;

    /**
     * Vertical coordinate
     * @var double
     */
    public $y;

    /**
     * Passengers inside
     * @var Passenger[]
     */
    public $passengers;

    /**
     * Elevator state
     * @var integer
     */
    public $state;

    /**
     * Current speed
     * @var double 
     */
    public $speed;

    /**
     * Current floor
     * @var integer
     */
    public $floor;

    /**
     * Next (destignated) floor
     * @var integer
     */
    public $nextFloor;

    /**
     * Ticks elevator holding on current floor
     * @var integer
     */
    public $timeOnFloor;

    /**
     * ???
     * @var string
     */
    public $type;

    /**
     * Current commands
     * @var string[]
     */
    public $messages = [];

    /**
     * 
     * @param integer $id
     * @param double $y
     * @param Passenger[] $passengers
     * @param integer $state
     * @param double $speed
     * @param integer $floor
     * @param integer $nextFloor
     * @param integer $timeOnFloor
     * @param string $type
     */
    function __construct($id, $y, $passengers, $state, $speed, $floor, $nextFloor, $timeOnFloor, $type)
    {
        $this->id = $id;

        $this->y = $y;

        $this->passengers = array_map(function (Passenger $p) {
            return new Passenger($p->id, $p->elevator, $p->x, $p->y, $p->state, $p->timeToAway, $p->fromFloor, $p->destFloor, $p->type, $p->floor);
        }, $passengers);

        $this->state = $state;

        $this->speed = $speed;

        $this->floor = $floor;

        $this->nextFloor = $nextFloor;

        $this->timeOnFloor = $timeOnFloor;

        $this->type = $type;
    }

    /**
     * Sets command 'go_to_floor'
     * @param integer $floor
     */
    public function goToFloor($floor)
    {
        $this->nextFloor = $floor;
        $this->messages[] = [
            'command' => 'go_to_floor',
            'args' => [
                'elevator_id' => $this->id,
                'floor' => $floor,
            ],
        ];
    }

}

/**
 * Passenger (read-only)
 */
class Passenger
{
    
    /**
     * Passenger waiting for elevator
     */
    const STATE_WAITING_FOR_ELEVATOR = 1;
    
    /**
     * Passenger moving to destignated elevator
     */
    const STATE_MOVING_TO_ELEVATOR = 2;
    
    /**
     * Passenger returning to central point
     */
    const STATE_RETURNING = 3;
    
    /**
     * Passenger moving to floor using the stairway
     */
    const STATE_MOVING_TO_FLOOR = 4;
    
    /**
     * Passenger is in elevator
     */
    const STATE_USING_ELEVATOR = 5;
    
    /**
     * Passenger exiting from elevator
     */
    const STATE_EXITING = 6;

    /**
     * Passenger identifier
     * @var integer
     */
    public $id;

    /**
     * Elevator identifier (or null)
     * @var integer
     */
    public $elevatorId = null;

    /**
     * Horisontal coordinate
     * @var double
     */
    public $x;

    /**
     * Vertical coordinate
     * @var double
     */
    public $y;

    /**
     * Ticks to away
     * @var integer
     */
    public $timeToAway;

    /**
     * Current floor
     * @var integer
     */
    public $floor;

    /**
     * Floor passenger from
     * @var integer
     */
    public $fromFloor;

    /**
     * Passenger destignation floor
     * @var integer
     */
    public $destFloor;

    /**
     * ???
     * @var string
     */
    public $type;

    /**
     * Passenger state
     * @var integer
     */
    public $state;

    /**
     * Current commands
     * @var string[]
     */
    public $messages = [];

    function __construct($id, $elevatorId, $x, $y, $state, $timeToAway, $fromFloor, $destFloor, $type, $floor)
    {
        $this->id = $id;

        $this->elevatorId = $elevatorId;

        $this->x = $x;

        $this->y = $y;

        $this->timeToAway = $timeToAway;

        $this->floor = $floor;

        $this->fromFloor = $fromFloor;

        $this->destFloor = $destFloor;

        $this->type = $type;

        $this->state = $state;
    }

    /**
     * Push command 'set_elevator_to_passenger'
     * @param integer $elevatorId
     */
    public function setElevator($elevatorId)
    {
        $this->elevatorId = $elevatorId;
        $this->messages[] = [
            'command' => 'set_elevator_to_passenger',
            'args' => [
                'passenger_id' => $this->id,
                'elevator_id' => $elevatorId,
            ],
        ];
    }

    /**
     * Checks passenger has destignated elevator
     * @return bool
     */
    public function hasElevator(): bool
    {
        return !is_null($this->elevatorId);
    }

}

/**
 * Debugger
 * @property stirng[] $messages
 */
class Debug
{

    /**
     *
     * @var string[]
     */
    private $_messages = [];

    /**
     * Return and clear messages, or return null
     * @param string $name
     * @return mixed
     */
    function __get($name)
    {
        if ($name == 'messages') {
            $messages = $this->_messages;
            $this->_messages = [];
            return $messages;
        }
        return null;
    }

    /**
     * Push command 'log'
     * @param string $text
     */
    public function log($text)
    {
        $this->_messages[] = [
            'command' => 'log',
            'args' => [
                'text' => (string) $text,
            ],
        ];
    }

    /**
     * Push command 'exception'
     * @param mixed $text
     */
    public function exception($text)
    {
        $this->_messages[] = [
            'command' => 'exception',
            'args' => [
                'text' => (string) $text,
            ],
        ];
    }

}

/**
 * Api
 */
class Api
{

    /**
     * Debugger
     * @var Debug
     */
    public $debug;

    /**
     * Strategy object
     * @var BaseStrategy
     */
    public $strategy;

    /**
     * 
     */
    function __construct()
    {
        $this->debug = new Debug();
        $this->strategy = null;

        try {
            @eval("require('strategy.php');");
            $this->strategy = new Strategy($this->debug);
        } catch (ParseError $e) {
            $this->debug->exception((string) $e);
        }
    }

    /**
     * Convert array of json-objects to array of Passenger objects
     * @param array $passengers
     * @return type
     */
    private function parsePassengers(array $passengers)
    {
        return array_map(function ($p) {
            return new Passenger(
                    $p->id, $p->elevator, $p->x, $p->y, $p->state, $p->time_to_away, $p->from_floor, $p->dest_floor, $p->type, $p->floor
            );
        }, $passengers);
    }

    /**
     * Convert array of json-objects to array of Elevator objects
     * @param stdClass[] $elevators
     * @return Elevator[]
     */
    private function parseElevators(array $elevators)
    {
        return array_map(function ($el) {
            return new Elevator(
                    $el->id, $el->y, $el->passengers, $el->state, $el->speed, $el->floor, $el->next_floor, $el->time_on_floor, $el->type
            );
        }, $elevators);
    }

    /**
     * Parse json-object and create objects of Passenger and Elevator
     * @param stdClass $state
     * @return array ['myPassengers' => Passenger[], 'myElevators' => Elevator[], 'enemyPassengers' => Passenger[], 'enemyElevators' => Elevator[]]
     */
    private function parseState(stdClass $state)
    {
        return [
            "myPassengers" => $this->parsePassengers($state->my_passengers),
            "myElevators" => $this->parseElevators($state->my_elevators),
            "enemyPassengers" => $this->parsePassengers($state->enemy_passengers),
            "enemyElevators" => $this->parseElevators($state->enemy_elevators),
        ];
    }

    /**
     * Process strategy turn
     * @param stdClass $state world state
     * @return string[] messages generated by strategy
     */
    public function turn(stdClass $state)
    {
        $data = $this->parseState($state);
        try {
            if ($this->strategy) {
                @eval('$this->strategy->onTick($data["myPassengers"], $data["myElevators"], $data["enemyPassengers"], $data["enemyElevators"]);');
            }
        } catch (Error $e) {
            $this->debug->exception((string) $e);
        }

        $tempResult = array_map(function($item) {
            return $item->messages;
        }, array_merge($data["myPassengers"], $data["myElevators"], $data["enemyPassengers"], array($this->debug)));

        $result = [];
        foreach ($tempResult as $tmp) {
            $result = array_merge($result, $tmp);
        }
        return $result;
    }

}
