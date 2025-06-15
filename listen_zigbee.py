#!/usr/bin/env python3

import configparser
import json
from pathlib import Path

from granary.common.communication import Zigbee2MQTTClient

if __name__ == "__main__":
    dir_path = Path(__file__).resolve().parent

    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    with open("{}/zb_devices.json".format(dir_path)) as f:
        zb_devices = json.load(f)
    print(zb_devices)

    zb_mqtt = Zigbee2MQTTClient(
        username=config.get("MQTT", "Username"),
        passwd=config.get("MQTT", "Password"),
        broker=config.get("MQTT", "Broker"),
        port=config.getint("MQTT", "Port"),
    )

    zb_mqtt.run()
