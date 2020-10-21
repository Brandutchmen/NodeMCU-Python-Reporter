import json
import serial
import time

port = "COM3"
rate = 57600
timeout_duration = 6  # 6 seconds
ser = serial.Serial(port, rate)

url = "localhost"

print("Starting")
for i in range(3):
    time.sleep(0.5)
    print(".")

def sendBatch(batch):
    print("Sending")
    for i in range(3):
        time.sleep(0.5)
        print(".")

    print(batch)

while True:
    timeout = time.time() + timeout_duration
    batch = list()
    while True:
        if time.time() > timeout:
            sendBatch(batch)
            break
        mac = ser.readline().decode("utf-8")[0:17]
        if len(mac) > 10:
            if mac not in batch:
                batch.append(mac)

