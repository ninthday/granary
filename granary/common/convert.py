#!/usr/bin/env python3
from datetime import datetime
from time import time


class GranaryConvert:
    def convert_timestamp(self, timestamp: int):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def get_datafile_name(self):
        return datetime.strftime(datetime.now(), "%Y-%m.db")
