#!/usr/bin/env python3

from pathlib import Path
from fastapi import FastAPI
from datetime import datetime
from granary.common.convert import GranaryConvert
from granary.storage.local_storage import GranaryStorage


app = FastAPI()

dir_path = Path(__file__).resolve().parent
conv = GranaryConvert()
datafile_name = conv.get_datafile_name()
local_storage = GranaryStorage(dir_path, datafile_name)


@app.get("/sensordata")
async def index_sensor_data(device_type: str, device_id: int, limit: int = 10):
    sensor_dara = []
    local_data = local_storage.get_device_data(device_type, device_id, limit)
    for row_data in local_data:
        sensor_dara.append(
            {
                "rowId": row_data[0],
                "deviceId": row_data[1],
                "dataTime": conv.convert_timestamp(row_data[2]),
                "temperature": row_data[3],
                "humidity": row_data[4],
                "battery": row_data[5],
            }
        )
    return {"sensorData": sensor_dara}
