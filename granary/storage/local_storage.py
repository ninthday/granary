#!/usr/bin/env python3

import sqlite3
from datetime import datetime
from pathlib import Path
from shutil import copyfile


class GranaryStorage:
    def __init__(self, dir_path: str, sqlite_name: str):
        try:
            self.chk_datafile(dir_path, sqlite_name)

            conn_path = "{}/data/{}".format(dir_path, sqlite_name)
            self.conn = sqlite3.connect(conn_path)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            raise

    def chk_datafile(self, dir_path: str, sqlite_name: str):
        bak_path = Path("{}/data/{}".format(dir_path, sqlite_name))
        src_path = Path("{}/data/empty.db.example".format(dir_path))
        try:
            if src_path.exists():
                if not bak_path.exists():
                    copyfile(src_path, bak_path)
                    print("Copy local backup file: {}!".format(sqlite_name))
                    # event_logger.event("Copy local backup file: {}!".format(filename))
            else:
                print("File empty.db wasn't exist!")
                # err_logger.error("File empty.db wasn't exist!")
        except Exception as e:
            print("Check datafile Exception:" + repr(e))
            # err_logger.exception("Exception:" + repr(e))

    def local_backup(self, device_data: dict):

        try:
            if device_data["type"] == "lywsd02mmc":
                self._store_lywsd02mmc(device_data["data"])
            elif device_data["type"] == "lywsd03mmc":
                self._store_lywsd03mmc(device_data["data"])
        except Exception as e:
            print("Exception:" + repr(e))
            raise

    def _store_lywsd02mmc(self, device_id: int, data: dict):
        sql = "INSERT INTO `lywsd02mmc` (`device_id`, `localts`, `air_temperature`, `air_humidity`, `battery`, `rssi`)\
               VALUES (?, ?, ?, ?, ?, ?);"
        params = (
            device_id,
            data["local_timestamp"],
            data["air_temperature"],
            data["air_humidity"],
            data["battery"],
            data["rssi"],
        )
        self._insert_sqlite(sql, params)

    def _store_lywsd03mmc(self, data: dict):
        sql = "INSERT INTO `lywsd03mmc` (`device_id`, `localts`, `air_temperature`, `air_humidity`, `battery`, `rssi`)\
               VALUES (?, ?, ?, ?, ?, ?);"
        params = (
            data["device_id"],
            data["local_timestamp"],
            data["air_temperature"],
            data["air_humidity"],
            data["battery"],
            data["rssi"],
        )
        self._insert_sqlite(sql, params)

    def _insert_sqlite(self, sql_statm: str, params: tuple):
        try:
            self.cur.execute(sql_statm, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            raise

    def check_alltable(self):
        tables_to_ignore = ["sqlite_sequence"]
        sql = "SELECT `name` FROM `sqlite_master` WHERE `type`='table'"
        self.cur.execute(sql)
        tables = map(lambda t: t[0], self.cur.fetchall())
        upload_tables = list()
        for table in tables:
            if table in tables_to_ignore:
                continue
            q = "SELECT COUNT(*) FROM {}".format(table)
            self.cur.execute(q)
            num_rows = self.cur.fetchone()[0]
            if num_rows > 0:
                upload_tables.append(table)
        return upload_tables

    def show_local_tables(self):
        """
        回傳目前 sqlite 的資料表，無論有沒有資料
        """
        tables_to_ignore = ["sqlite_sequence"]
        sql = "SELECT `name` FROM `sqlite_master` WHERE `type`='table'"
        self.cur.execute(sql)
        tables = map(lambda t: t[0], self.cur.fetchall())
        local_tables = list()
        for table in tables:
            if table in tables_to_ignore:
                continue
            local_tables.append(table)
        return local_tables

    def get_data(self, table_name: str):
        """
        取得指定資料表的所有資料
        Keyword arguments:
            table_name (string) -- 資料表名稱
        Returns:
            指定資料表目前所有的內容
        """
        sql = "SELECT * FROM {}".format(table_name)
        self.cur.execute(sql)
        local_data = self.cur.fetchall()
        return local_data

    def del_data(self, table_name: str, row_id: int):
        """
        刪除指定資料表及編號的資料
        Keyword arguments:
            table_name (string) -- 資料表名稱
            row_id (int) -- 記錄編號
        Returns:
            指定資料表目前所有的內容
        """
        sql = "DELETE FROM `{}` WHERE `id`={}".format(table_name, row_id)
        self.cur.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


class AgriLocalFile:
    def __init__(self, dir_path):
        self._dir_path = dir_path

    def keep_future_data(self, read_time, data_ts, data_string):
        """記錄未來時間的原始資料
        Args:
            read_time (string): 資料讀取時的時間字串
            data_ts (int): device 的資料時間（data_timestamp）
            data_string (string): 要記錄的原始資料字串
        """
        log_filename = "{}/data/future_data.log".format(self._dir_path)
        data_time = datetime.fromtimestamp(data_ts).strftime("%Y-%m-%d %H:%M:%S")
        with open(log_filename, "a") as outfile:
            msg = "{0}--<<--{1}: {2}\n".format(read_time, data_time, data_string)
            outfile.write(msg)

    def keep_garbled_data(self, read_time, garbled_text):
        """記錄 Serial 取得的亂碼內容
        Args:
            read_time (string): 資料讀取時的時間字串
            garbled_text (string): 發生亂碼的字串內容
        """
        log_filename = "{}/data/garbled_data.log".format(self._dir_path)
        with open(log_filename, "a") as outfile:
            msg = "{0}: {1}\n".format(read_time, garbled_text)
            outfile.write(msg)
