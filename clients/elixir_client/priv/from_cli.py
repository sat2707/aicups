import json
js = [{u'args': {u'elevator_id': 1, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 1, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 1, u'floor': 6}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 2, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 2, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 3, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 3, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 4, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'elevator_id': 4, u'floor': 1}, u'command': u'go_to_floor'}, {u'args': {u'passenger_id': 8, u'elevator_id': 1}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 8, u'elevator_id': 2}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 8, u'elevator_id': 3}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 8, u'elevator_id': 4}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 10, u'elevator_id': 1}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 10, u'elevator_id': 2}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 10, u'elevator_id': 3}, u'command': u'set_elevator_to_passenger'}, {u'args': {u'passenger_id': 10, u'elevator_id': 4}, u'command': u'set_elevator_to_passenger'}]
print json.dumps(js)