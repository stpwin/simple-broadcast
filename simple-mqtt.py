import paho.mqtt.client as mqtt
import struct
import json


MQTT_HOST = "192.168.1.3"
MQTT_PORT = 1883

mqttclient = mqtt.Client()
mqttclient.connect(MQTT_HOST, MQTT_PORT)

irCommand = {
    "power": 255,
    "mode": 255,
    "fan": 255,
    "temp": 24,
    "h_swing": 255,
    "v_swing": 255,
    "turbo": False
}

ir = json.dumps(irCommand, separators=(',', ':'))
print(ir)
# mqttclient.publish("my-unoEthernet/RELAY1_CMD", struct.pack('i', 1))
mqttclient.publish("my-unoEthernet/IR_CMD", ir)


def on_message_relay0(mosq, obj, msg):
    # print(msg.topic, msg.payload)
    try:
        result = struct.unpack('i', msg.payload)[0]
        print("%s > %r" % (msg.topic, result))
    except:
        print("on_message_relay0 unpack fail")


def on_message_relay1(mosq, obj, msg):
    # print(msg.topic, msg.payload)
    try:
        result = struct.unpack('i', msg.payload)[0]
        print("%s > %r" % (msg.topic, result))
    except:
        print("on_message_relay1 unpack fail")


def on_message_float(mosq, obj, msg):
    try:
        result = struct.unpack('f', msg.payload)[0]
        print("%s > %.2f" % (msg.topic, result))
    except:
        print("on_message_float unpack fail")


def on_message_temperature(mosq, obj, msg):
    try:
        result = struct.unpack('f', msg.payload)[0]
        print("%s > %.2f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_temperature unpack fail")


def on_message_humiduty(mosq, obj, msg):
    try:
        result = struct.unpack('f', msg.payload)[0]
        print("%s > %.2f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_humiduty unpack fail")


def on_message_ambient(mosq, obj, msg):
    return
    try:
        result = struct.unpack('f', msg.payload)[0]
        print("%s > %.4f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_ambient unpack fail")


def on_message_bmpTemperature(mosq, obj, msg):
    try:
        result = struct.unpack('f', msg.payload)[0]
        print("%s > %.0f \u00B0C" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_temperature unpack fail")


def on_message_pressure(mosq, obj, msg):
    try:
        result = struct.unpack('f', msg.payload)[0]
        pressurehPa = result / 100.0
        print("%s > %.0f hPa" % (msg.topic, pressurehPa))
        print("Approx. Altitude: %.0f m" % calcAltitude(pressurehPa, 1013.25))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_pressure unpack fail")


def on_message(mosq, obj, msg):
    pass
    # print("WHAT")
    print("%s > %s" % (msg.topic, msg.payload))


def calcAltitude(pressurehPa, seaLevelhPa):
    return 44330 * (1.0 - pow(pressurehPa / seaLevelhPa, 0.1903))


mqttclient.message_callback_add(
    "device/my-unoEthernet/relay0", on_message_relay0)

mqttclient.message_callback_add(
    "device/my-unoEthernet/relay1", on_message_relay1)

mqttclient.message_callback_add(
    "device/my-unoEthernet/float", on_message_float)

mqttclient.message_callback_add(
    "device/my-unoEthernet/temperature", on_message_temperature)

mqttclient.message_callback_add(
    "device/my-unoEthernet/humiduty", on_message_humiduty)

mqttclient.message_callback_add(
    "device/my-unoEthernet/ambient", on_message_ambient)

mqttclient.message_callback_add(
    "device/my-unoEthernet/pressure", on_message_pressure)

mqttclient.message_callback_add(
    "device/my-unoEthernet/bmpTemperature", on_message_bmpTemperature)

mqttclient.on_message = on_message
mqttclient.subscribe("device/my-unoEthernet/#")
mqttclient.loop_forever()
