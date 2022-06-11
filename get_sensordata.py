#!/usr/bin/env python3
import configparser
import json
from threading import local
from bluepy.btle import BTLEDisconnectError
from lywsd03mmc import Lywsd03mmcClient
from lywsd02 import Lywsd02Client
from pathlib import Path
from datetime import datetime
from time import time, sleep
from granary.storage.local_storage import GranaryStorage
from granary.common.logging import EventLogger, ErrorLogger


def init():
    global dir_path
    global event_logger
    global err_logger

    dir_path = Path(__file__).resolve().parent

    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    # 錯誤記錄檔
    err_logger = ErrorLogger(config["LogPath"]["File_path"], config["Granary"]["Name"])

    # 事件記錄檔
    event_logger = EventLogger(
        config["LogPath"]["File_path"], config["Granary"]["Name"]
    )


def get_data(mac_address: str, type: str, device_id: int) -> dict:
    try_times = 0
    loop = True
    sensor_data = {}

    if type == "lywsd03mmc":
        client = Lywsd03mmcClient(mac_address)
        while loop:
            try:
                data = client.data
                sensor_data["temperature"] = data.temperature
                sensor_data["humidity"] = data.humidity
                sensor_data["battery"] = data.battery
                loop = False
                del client
                event_logger.scan("lywsd03mmc", device_id, try_times)
            except BTLEDisconnectError as err:
                print("Error:" + repr(err))
                try_times += 1
                print("--> Try time: {}".format(try_times))
                sleep(1)
                continue
    elif type == "lywsd02mmc":
        client = Lywsd02Client(mac_address)
        while loop:
            try:
                with client.connect():
                    data = client.data
                    sensor_data["temperature"] = data.temperature
                    sensor_data["humidity"] = data.humidity
                    sensor_data["battery"] = client.battery

                loop = False
                del client
                event_logger.scan("lywsd02mmc", device_id, try_times)
            except BTLEDisconnectError as err:
                print("Error:" + repr(err))
                try_times += 1
                print("--> Try time: {}".format(try_times))
                sleep(1)
                continue

    return sensor_data


def get_now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def get_datafile_name():
    return datetime.strftime(datetime.now(), "%Y-%m.db")


if __name__ == "__main__":

    datafile_name = get_datafile_name()
    local_storage = GranaryStorage(dir_path, datafile_name)

    devices_filepath = "{}/devices.json".format(dir_path)
    try:
        with open(devices_filepath, "r") as file:
            devices = json.load(file)
    except FileNotFoundError as err:
        print("Exception:" + repr(err))
        devices = None

    if len(devices["lywsd03mmc"]) > 0:
        for device in devices["lywsd03mmc"]:
            sensor_data = get_data(device["mac"], "lywsd03mmc", device["id"])
            device_data = {
                "device_id": int(device["id"]),
                "type": "lywsd03mmc",
                "data": {
                    "local_timestamp": int(time()),
                    "air_temperature": sensor_data["temperature"],
                    "air_humidity": sensor_data["humidity"],
                    "battery": sensor_data["battery"],
                    "rssi": 0,
                },
            }
            local_storage.local_backup(device_data)
            print(device_data)

    if len(devices["lywsd02mmc"]) > 0:
        for device in devices["lywsd02mmc"]:
            sensor_data = get_data(device["mac"], "lywsd02mmc", device["id"])
            device_data = {
                "device_id": int(device["id"]),
                "type": "lywsd02mmc",
                "data": {
                    "local_timestamp": int(time()),
                    "air_temperature": sensor_data["temperature"],
                    "air_humidity": sensor_data["humidity"],
                    "battery": sensor_data["battery"],
                    "rssi": 0,
                },
            }
            local_storage.local_backup(device_data)
            print(device_data)
