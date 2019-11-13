import paho.mqtt.client as mqtt
import json
import struct

MQTT_HOST = "isysforce.myddns.me"
MQTT_PORT = 8883

mqttclient = mqtt.Client()
mqttclient.connect(MQTT_HOST, MQTT_PORT)

PUB = "my-unoEthernet/RELAY_CMD/1"
print(f"Publish to {PUB}")

irCommand = {
    "power": 255,
    "mode": 255,
    "fan": 255,
    "temp": 24,
    "h_swing": 255,
    "v_swing": 255,
    "turbo": False
}

payload = json.dumps(irCommand, separators=(',', ':'))
# print(payload)
mqttclient.publish(PUB, struct.pack('B', 1))
