import paho.mqtt.client as mqtt
import os


import time

DEVICE_IP = "192.168.1.9"
MQTT_HOST = "192.168.1.3"
MQTT_PORT = 1883

mqttclient = mqtt.Client()
mqttclient.will_set("status/myphone", "LOST CONNECTION")
mqttclient.connect(MQTT_HOST, MQTT_PORT)

while True:

    response = os.system("ping -c1 " + DEVICE_IP)

    if response == 0:
        print(DEVICE_IP, 'is up!')
        mqttclient.publish("status/myphone", "online", True)
    else:
        print(DEVICE_IP, 'is down!')
        mqttclient.publish("status/myphone", "offline", True)

    time.sleep(5)
