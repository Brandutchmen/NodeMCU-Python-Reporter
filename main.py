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

timeout_duration = getConfig("timeout", 60)  # 60 seconds default
ser = serial.Serial(getConfig("port", "COM3"), getConfig("rate", 57600))

print("Starting")
for i in range(3):
    time.sleep(0.3)
    print(".")

def sendBatch(batch):
    print(batch)
    requests.post(config["url"], json=batch)

try:
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
except serial.serialutil.SerialException:
    # We need to report downtime
    print("CONNECTION BROKEN: Sending report to IFTTT:")
    requests.post(str("https://maker.ifttt.com/trigger/") + str(config["ifttt_event"] + str("/with/key/") +str(config["ifttt_secret"])))