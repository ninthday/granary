#!/usr/bin/env python3
import configparser
import json
from threading import local
from bluepy.btle import BTLEDisconnectError
from lywsd03mmc import Lywsd03mmcClient
from pathlib import Path

from datetime import datetime
from time import time, sleep
from granary.storage.local_storage import GranaryStorage


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


def _get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def get_datafile_name():
    return datetime.strftime(datetime.now(), "%Y-%m.db")


if __name__ == "__main__":
    dir_path = Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    datafile_name = get_datafile_name()
    local_storage = GranaryStorage(dir_path, datafile_name)

    devices_filepath = "{}/devices.json".format(dir_path)
    try:
        with open(devices_filepath, "r") as file:
            devices = json.load(file)
    except FileNotFoundError as err:
        print("Exception:" + repr(err))
        devices = None

    for device in devices["lywsd03mmc"]:
        sensor_data = get_data(device["mac"])
        device_data = {
            "device_id": int(device["id"]),
            "type": "lywsd03mmc",
            "data": {
                "local_timestamp": int(time()),
                "air_temperature": sensor_data.temperature,
                "air_humidity": sensor_data.humidity,
                "battery": sensor_data.battery,
                "rssi": 0,
            },
        }
        local_storage.local_backup(device_data)
        print("Temperature: " + str(sensor_data.temperature))
        print("Humidity: " + str(sensor_data.humidity))
        print("Battery: " + str(sensor_data.battery))
        print(device_data)
