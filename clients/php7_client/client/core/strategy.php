<?php
    require('base_strategy.php');

    class Strategy extends BaseStrategy {
        public function on_tick($my_passengers, $my_elevators, $enemy_passengers, $enemy_elevators) {
            foreach ($my_elevators as $elevator) {
                foreach ($my_passengers as $passenger) {
                    if ($passenger->state < 5) {
                        if ($elevator->state != 1) {
                            $elevator->go_to_floor($passenger->from_floor);
                        }
                        if ($elevator->floor == $passenger->from_floor) {
                            $passenger->set_elevator($elevator);
                        }
                    }
                    if (count($elevator->passengers) > 0 && $elevator->state != 1) {
                        $elevator->go_to_floor($elevator->passengers[0]->dest_floor);
                    }
                }
            }
        }
    }
?>
