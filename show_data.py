import configparser
import json
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime
from granary.common.convert import GranaryConvert
from granary.storage.local_storage import GranaryStorage


if __name__ == "__main__":
    parser = ArgumentParser(description="CrowdTangle list accounts")
    parser.add_argument(
        "-n", "--num", help="number of rows to show", dest="row_num", type=int
    )
    args = parser.parse_args()

    dir_path = Path(__file__).resolve().parent
    config = configparser.ConfigParser()
    config.read("{}/config.ini".format(dir_path))

    conv = GranaryConvert()
    datafile_name = conv.get_datafile_name()
    local_storage = GranaryStorage(dir_path, datafile_name)

    devices_filepath = "{}/devices.json".format(dir_path)
    try:
        with open(devices_filepath, "r") as file:
            devices = json.load(file)
    except FileNotFoundError as err:
        print("Exception:" + repr(err))
        devices = None

    for device_type in devices:
        print("=== {} ===============".format(device_type))
        for device in devices[device_type]:
            local_data = local_storage.get_device_data(
                device_type, device["id"], args.row_num
            )
            print("Device ID: {}".format(device["id"]))
            for row_data in local_data:
                print(
                    "row: {row_id}, device: {device_id}, time: {data_time}, temperature: {temperature}, humidity: {humidity}, battery: {battery}".format(
                        row_id=row_data[0],
                        device_id=row_data[1],
                        data_time=conv.convert_timestamp(row_data[2]),
                        temperature=row_data[3],
                        humidity=row_data[4],
                        battery=row_data[5],
                    )
                )
