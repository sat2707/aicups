<?php
    // (Лифт) атрибуты только для чтения
    class Elevator {
        function __construct($id, $y, $passengers, $state, $speed, $floor, $next_floor, $time_on_floor, $type ) {
            // идентификатор лифта (0, 1, 2)
            $this->id = $id;

            // координата по вертикали
            $this->y = $y;

            $this->passengers = array_map(function ($p) {
                return new Passenger(
                    $p->id,
                    $p->elevator,
                    $p->x,
                    $p->y,
                    $p->state,
                    $p->time_to_away,
                    $p->from_floor,
                    $p->dest_floor,
                    $p->type,
                    $p->floor,
                    $p->weight);
            }, $passengers);


            $this->state = $state;

            $this->speed = $speed;

            $this->floor = $floor;

            $this->next_floor = $next_floor;

            $this->time_on_floor = $time_on_floor;

            $this->type = $type;

            $this->messages = array();
        }

        public function go_to_floor($floor) {
            $this->next_floor = $floor;
            array_push($this->messages, array(
                'command' => 'go_to_floor',
                'args' => array(
                    'elevator_id' => $this->id,
                    'floor' => $floor
                )
            ));

        }
    }


    // (Пассажир) атрибуты только для чтения
    class Passenger {
        function __construct($id, $elevator, $x, $y, $state, $time_to_away, $from_floor, $dest_floor, $type, $floor, $weight) {
            // идентификатор пассажира
            $this->id = $id;

            // идентификатор лифта (null если нет)
            $this->elevator = $elevator;

            // координаты
            $this->x = $x;
            $this->y = $y;
            $this->time_to_away = $time_to_away;

            // этаж "откуда" и этаж "куда"
            $this->floor = $floor;
            $this->from_floor = $from_floor;
            $this->dest_floor = $dest_floor;

            $this->type = $type;

            $this->state = $state;
            $this->weight = $weight;
            $this->messages = array();
        }

        // назначить пассажиру лифт
        public function set_elevator($elevator) {
            $this->elevator = $elevator;
            array_push($this->messages, array(
                'command' => 'set_elevator_to_passenger',
                'args' => array(
                    'passenger_id' => $this->id,
                    'elevator_id' => $elevator->id,
                )
            ));
        }

        // проверить, есть ли лифт у пассажира
        public function has_elevator() : bool {
            if ($this->elevator !== '' && $this->elevator !== null) {
                return true;
            }
            return false;
        }

    }


    class Debug {
        private  $_messages = array();

        function __get($name) {
            if ($name == 'messages') {
                $messages = $this->_messages;
                $this->_messages = array();
                return $messages;
            }
            return null;
        }

        // Отладка в консоль
        public function log($text) {
            array_push($this->_messages, array(
                'command' => 'log',
                'args' => array(
                    'text' => (string) $text,
                )
            ));
        }

        public function exception ($text) {
            array_push($this->_messages, array(
                'command' => 'exception',
                'args' => array(
                    'text' => urlencode((string) $text),
                )
            ));
        }
    }


    class Api {
        function __construct() {

            $this->debug = new Debug();
            $this->strategy = null;

            try {
                @eval("require('strategy.php');");
                $this->strategy = new Strategy($this->debug);
            } catch (ParseError $e) {
                $this->debug->exception((string) $e);
            }
        }

        public function parse_state($state) {
            $my_passengers = $state->my_passengers;
            $my_passengers = array_map(function ($p) {
                return new Passenger(
                    $p->id,
                    $p->elevator,
                    $p->x,
                    $p->y,
                    $p->state,
                    $p->time_to_away,
                    $p->from_floor,
                    $p->dest_floor,
                    $p->type,
                    $p->floor,
                    $p->weight
                );
            }, $my_passengers);

            $my_elevators = $state->my_elevators;
            $my_elevators = array_map(function ($el) {
                return new Elevator(
                    $el->id,
                    $el->y,
                    $el->passengers,
                    $el->state,
                    $el->speed,
                    $el->floor,
                    $el->next_floor,
                    $el->time_on_floor,
                    $el->type
                );
            }, $my_elevators);

            $enemy_passengers = $state->enemy_passengers;
            $enemy_passengers = array_map(function ($p) {
                return new Passenger(
                    $p->id,
                    $p->elevator,
                    $p->x,
                    $p->y,
                    $p->state,
                    $p->time_to_away,
                    $p->from_floor,
                    $p->dest_floor,
                    $p->type,
                    $p->floor,
                    $p->weight
                );
            }, $enemy_passengers);

            $enemy_elevators = $state->enemy_elevators;
            $enemy_elevators = array_map(function ($el) {
                return new Elevator(
                    $el->id,
                    $el->y,
                    $el->passengers,
                    $el->state,
                    $el->speed,
                    $el->floor,
                    $el->next_floor,
                    $el->time_on_floor,
                    $el->type
                );
            }, $enemy_elevators);

            return array("my_passengers" => $my_passengers,
                         "my_elevators" => $my_elevators,
                         "enemy_passengers" => $enemy_passengers,
                         "enemy_elevators" => $enemy_elevators);
        }

        public function turn($state) {
            $data = $this->parse_state($state);
            try {
                if ($this->strategy) {
                    @eval('$this->strategy->on_tick($data["my_passengers"], $data["my_elevators"], $data["enemy_passengers"], $data["enemy_elevators"]);');
                }
            } catch (Error $e) {
                $this->debug->exception((string) $e);
            }
            $temp_result = array_map(function($item) {
                return $item->messages;
            }, array_merge($data["my_passengers"], $data["my_elevators"], $data["enemy_passengers"], array($this->debug)));

            $result = array();
            foreach ($temp_result as $tmp) {
                $result = array_merge($result, $tmp);
            }
            return $result;
        }
    }
?>
