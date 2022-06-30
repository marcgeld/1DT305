#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# install: pip3 install paho-mqtt

import random
import paho.mqtt.client as mqtt
import time
import os
import sys

import config

client_id = f'python-mqtt-{random.randint(0, 1000)}'


# onConnect
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)


# Set Connecting Client ID
client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set(config.USER, config.PASS)
client.on_connect = on_connect
client.connect(config.BROKER, config.PORT)

# create a run loop to get the async callback
client.loop_start()

# Wait for connection setup to complete
time.sleep(2)

topic = config.TOPIC
msg = f"messages to {topic}"
result = client.publish(topic, msg)
status = result[0]
if status == 0:
  print(f"Send `{msg}` to topic `{topic}`")
else:
  print(f"Failed to send message to topic {topic}")

client.loop_stop()
