#!/usr/bin/env python3
import configparser
import json
from bluepy.btle import BTLEDisconnectError
from lywsd03mmc import Lywsd03mmcClient
from pathlib import Path
from time import sleep


def get_data(mac_address: str):
    client = Lywsd03mmcClient(mac_address)
    try_times = 0
    loop = True
    while loop:
        try:
            data = client.data
            loop = False
            del client
        except BTLEDisconnectError as err:
            print("Error:" + repr(err))
            try_times += 1
            print("--> Try time: {}".format(try_times))
            sleep(1)
            continue
    return data


if __name__ == "__main__":
    dir_path = Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    devices_filepath = "{}/devices.json".format(dir_path)
    try:
        with open(devices_filepath, "r") as file:
            devices = json.load(file)
    except FileNotFoundError as err:
        print("Exception:" + repr(err))
        devices = None

    for device in devices["lywsd03mmc"]:
        data = get_data(device["mac"])
        print("Temperature: " + str(data.temperature))
        print("Humidity: " + str(data.humidity))
        print("Battery: " + str(data.battery))
