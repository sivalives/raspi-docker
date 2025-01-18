curl -X POST -H "Content-Type: application/json" -d   '{"message": {"light_state": "on"}}' http://localhost:5000/publish?routing_key=led_control
curl -X POST -H "Content-Type: application/json" -d   '{"message": {"light_state": "off"}}' http://localhost:5000/publish?routing_key=led_control

