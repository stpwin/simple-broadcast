from __future__ import print_function
import socket
import time
import thread
import json

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
# server.settimeout(0.2)
server.bind(("", 44444))
# server.listen(5)
# server.setblocking(False)


def on_new_client(socket):
    while True:
        msg = socket.recv(1024)
        print("\n" + msg + "\n")
        print("", end="\r")

    socket.close()


thread.start_new_thread(on_new_client, (server,))

SECRET = "FSTOP_DEVICE"

data = {
    'secret': SECRET,
    'mqtthost': "192.168.1.3",
    'mqttport': 1883
}

dataserialized = json.dumps(data, separators=(",", ":"))
print(len(dataserialized))

couter = 0
while True:
    couter += 1

    server.sendto(dataserialized, ('<broadcast>', 37020))

    print("no: %s" % (couter), end='\r')
    # if couter == 10:
    break
    time.sleep(5)
