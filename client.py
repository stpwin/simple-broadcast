from __future__ import print_function
import socket
import paho.mqtt.client as mqtt
import json
import uuid
import time

DEVICE_ID = str(uuid.uuid1())
ALIAS = "MY_ALIAS"

SECRET = "FSTOP_DEVICE"
connectpayload = {
    'alias': "My Temperature sensor",
    "device_info": "temperature sensor"
}

mqttclient = mqtt.Client()
mqttclient.will_set("status/" + DEVICE_ID, "LOST CONNECTION")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))


recieved_count = 0
while True:
    print("Waiting for server broadcast...")
    data, addr = client.recvfrom(1024)
    recieved_count += 1

    print("recieved: %s >> %s" %
          (addr, data))
    deserialized = json.loads(data)
    print("deserialized: " + deserialized['secret'])
    if (deserialized['secret'] == SECRET):
        print("Secret: OK")
        client.sendto(b"Hello", addr)
        print("Connect to mqtt server...")
        mqttclient.connect(
            deserialized["mqtthost"], deserialized["mqttport"])
        print("Sending information to mqtt server...")
        mqttclient.publish(
            "connect/" + DEVICE_ID, json.dumps(connectpayload), retain=True)

        print("Sending keepAlive to mqtt server...")
        while True:
            mqttclient.publish("status/" + DEVICE_ID, "online")
            time.sleep(3)
        break
    print("Secret: mismatch")
