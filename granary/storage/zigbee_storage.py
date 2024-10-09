#!/usr/bin/env python3

import sqlite3
from pathlib import Path
from shutil import copyfile


class ZigbeeCacheStore:
    def __init__(self, dir_path: str, sqlite_name: str):
        try:
            self.chk_datafile(dir_path, sqlite_name)

            conn_path = f"{dir_path}/data/{sqlite_name}"
            self._conn = sqlite3.connect(conn_path)
            self.cur = self._conn.cursor()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            raise

    def chk_datafile(self, dir_path: Path, sqlite_name: str):
        # bak_path = Path(f"{dir_path}/data/{sqlite_name}")
        bak_path = dir_path.joinpath(f"data/{sqlite_name}")
        src_path = dir_path.joinpath("data/empty.db.example")
        try:
            if src_path.exists():
                if not bak_path.exists():
                    copyfile(src_path, bak_path)
                    print(f"Copy local backup file: {sqlite_name}!")
            else:
                print("File empty.db wasn't exist!")
        except Exception as e:
            print("Check datafile Exception:" + repr(e))

    def __del__(self):
        if self._conn:
            self._conn.close()
