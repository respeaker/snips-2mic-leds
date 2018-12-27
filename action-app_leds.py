#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import pixels
import os

try:
    addr_35 = [a == "UU\n" for a in os.popen("i2cdetect -y  1 0x35 0x35 | grep UU | awk '{print $2}'").readlines()]
    addr_35.append(False)
    addr_3b = [a == "UU\n" for a in os.popen("i2cdetect -y  1 0x3b 0x3b | grep UU | awk '{print $2}'").readlines()]
    addr_3b.append(False)
    addr_1a = [a == "UU\n" for a in os.popen("i2cdetect -y  1 0x1a 0x1a | grep UU | awk '{print $2}'").readlines()]
    addr_1a.append(False)
    addr = [addr_1a, addr_35, addr_3b]

    if addr[0][0] and (not addr[1][0]):
        # 2mic
        import pixels
        leds = pixels.pixels
        print('using 2mic')

    elif addr[2][0]:
        # 4mic or 6mic
        print('using 4mic or 6mic')
        from gpiozero import LED
        led = LED(5)
        led.on()
        from pixel_ring import pixel_ring
        leds = pixel_ring
    else:
        print("can't detect pi hat")
        os._exit(1)

except Exception as e:
    print("Error: {}".format(e))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/broker/version")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "hermes/hotword/toggleOff":
        leds.wakeup()
    elif msg.topic == "hermes/asr/textCaptured":
        leds.think()
    elif msg.topic == "hermes/nlu/intentParsed":
        leds.off()
    elif msg.topic == "hermes/tts/say":
        leds.speak()
    elif msg.topic == "hermes/tts/sayFinished":
        leds.off()
    elif msg.topic == "hermes/hotword/toggleOn":
        leds.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

topics = [("hermes/intent/#", 0), ("hermes/hotword/#", 0), ("hermes/asr/#", 0), ("hermes/nlu/#", 0),
                  ("snipsmanager/#", 0), ("hermes/tts/#", 0)]


client.subscribe(topics)

client.loop_forever()



# MQTT_TOPIC_NLU = "hermes/nlu/"
# MQTT_TOPIC_HOTWORD = "hermes/hotword/"
# MQTT_TOPIC_ASR = "hermes/asr/"
# MQTT_TOPIC_DIALOG_MANAGER = "hermes/dialogueManager/"
# MQTT_TOPIC_SNIPSFILE = "snipsskills/setSnipsfile/"
# MQTT_TOPIC_INTENT = "hermes/intent/"
# MQTT_TOPIC_SESSION_QUEUED = MQTT_TOPIC_DIALOG_MANAGER + "sessionQueued"
# MQTT_TOPIC_SESSION_STARTED = MQTT_TOPIC_DIALOG_MANAGER + "sessionStarted"
# MQTT_TOPIC_SESSION_ENDED = MQTT_TOPIC_DIALOG_MANAGER + "sessionEnded"
