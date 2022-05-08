#!/usr/bin/env python3
import configparser
import json
from pathlib import Path
from lywsd03mmc import Lywsd03mmcClient

dir_path = Path(__file__).resolve().parent
config = configparser.ConfigParser()
config.read("{}/config.ini".format(dir_path))

devices_filepath = "{}/devices.json".format(dir_path)
try:
    with open(devices_filepath, "r") as file:
        devcies = json.load(file)
except FileNotFoundError as err:
    print("Exception:" + repr(err))
    devices = None


for device in devices["lywsd03mmc"]:
    client = Lywsd03mmcClient(device["mac"])

    data = client.data
    print("Temperature: " + str(data.temperature))
    print("Humidity: " + str(data.humidity))
    print("Battery: " + str(data.battery))
    print("Display units: " + client.units)


# if __name__ == "__main__":
