import paho.mqtt.client as mqtt
import struct
import json
import pyrebase
import time
config = {
    "apiKey": "AIzaSyBwfvkoffX7MNGrWrf7nYYQ9wmOwS5_yaI",
    "authDomain": "stpwin-home.firebaseapp.com",
    "databaseURL": "https://stpwin-home.firebaseio.com",
    "storageBucket": "stpwin-home.appspot.com",
    "messagingSenderId": "796798924451",
    "appId": "1:796798924451:web:f0c42c137da2bdb69cf116"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def dbUpdatePressure(pressure):
    db.child("device").child("bmp280-01").child(
        "pressure").child(int(time.time())).set(pressure)


def dbUpdateTemperature(temperature):
    db.child("device").child("bmp280-01").child(
        "temperature").child(int(time.time())).set(temperature)


MQTT_HOST = "isysforce.myddns.me"
MQTT_PORT = 8883

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

# ir = json.dumps(irCommand, separators=(',', ':'))
# print(ir)
# mqttclient.publish("my-unoEthernet/RELAY1_CMD", struct.pack('i', 1))
# mqttclient.publish("my-unoEthernet/IR_CMD", ir)


def on_message_relay(mosq, obj, msg):
    # print(msg.topic, msg.payload)
    print("%s > %r[RAW]" % (msg.topic, msg.payload))
    try:
        result = struct.unpack('B', msg.payload)[0]
        print("%s > %r" % (msg.topic, result))
    except:
        print("on_message_relay unpack fail")


def on_message_float(mosq, obj, msg):
    return
    print("%s[RAW] > %r" % (msg.topic, msg.payload))
    try:
        result = struct.unpack('<h', msg.payload)[0]
        print("%s > %i" % (msg.topic, result))
    except:
        print("on_message_float unpack fail")


def on_message_temperature(mosq, obj, msg):
    try:
        result = struct.unpack('i', msg.payload)[0]
        print("%s > %.2f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_temperature unpack fail")


def on_message_humiduty(mosq, obj, msg):
    try:
        result = struct.unpack('i', msg.payload)[0]
        print("%s > %.2f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_humiduty unpack fail")


def on_message_ambient(mosq, obj, msg):
    return
    try:
        result = struct.unpack('i', msg.payload)[0]
        print("%s > %.4f" % (msg.topic, result))
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_ambient unpack fail")


def on_message_bmpTemperature(mosq, obj, msg):
    try:
        result = struct.unpack('<h', msg.payload)[0]
        print("%s > %d \u00B0C" % (msg.topic, result))
        dbUpdateTemperature(result)
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_bmpTemperature unpack fail")


def on_message_pressure(mosq, obj, msg):
    # return
    try:
        # print("%s[RAW] > %r" % (msg.topic, msg.payload))

        result = struct.unpack('i', msg.payload)[0]
        # pressurehPa = int(result / 100.0)
        print("%s > %d hPa" % (msg.topic, result))
        # print("Approx. Altitude: %.0f m" % calcAltitude(pressurehPa, 1013.25))
        dbUpdatePressure(result)
        # print("%s > %s" % (msg.topic, msg.payload))
    except:
        print("on_message_pressure unpack fail")


def on_message(mosq, obj, msg):
    pass
    # print("WHAT")
    print("%s > %r" % (msg.topic, msg.payload))


def calcAltitude(pressurehPa, seaLevelhPa):
    return 44330 * (1.0 - pow(pressurehPa / seaLevelhPa, 0.1903))


mqttclient.message_callback_add(
    "device/my-unoEthernet/relay/#", on_message_relay)

# mqttclient.message_callback_add(
#     "device/my-unoEthernet/relay1", on_message_relay1)

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
