import json
import serial
import time
import requests

f = open('config.json')
config = json.load(f)

def getConfig(value, default):
    try:
        if config[value]:
            return config[value]
    except KeyError:
        return default

timeout_duration = getConfig("timeout", 60)  # 6 seconds
ser = serial.Serial(getConfig("port", "COM3"), getConfig("rate", 57600))

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
    try:
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
    except serial.serialutil.SerialException:
        # We need to report downtime
        requests.post(str("https://maker.ifttt.com/trigger/") + str(config["ifttt_name"] + str("/with/key/") +str(config["ifttt_secret"])    