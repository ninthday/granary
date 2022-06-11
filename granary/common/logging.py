#!/usr/bin/env python3
import logging
from logging import handlers


class EventLogger:
    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, logger_name):
        if logger_name != "":
            self._logger_name = "even.{0}".format(logger_name)
        else:
            raise ValueError("The given logger name is empty!")

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path=None):
        if file_path != "" or file_path is not None:
            self._file_path = file_path
        else:
            self._file_path = "/var/log/granary"

    def __init__(self, file_path, logger_name):
        file_formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        self.file_path = file_path
        self.logger_name = logger_name
        fully_path = "{file_path}/{filename}".format(
            file_path=self.file_path, filename="event.log"
        )
        log_handler = logging.handlers.RotatingFileHandler(
            fully_path, maxBytes=1048576, backupCount=5
        )
        log_handler.setFormatter(file_formatter)
        self._logger = logging.getLogger(self._logger_name)
        self._logger.setLevel(logging.WARNING)
        self._logger.addHandler(log_handler)

    def event(self, msg: str) -> None:
        self._logger.info(msg)

    def scan(self, device_type: str, device_id: int, scan_times: int) -> None:
        self._logger.info(
            "Scanned {device_type}({device_id}) -> {scan_times} times.".format(
                device_type=device_type, device_id=device_id, scan_times=scan_times
            )
        )


class ErrorLogger:
    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, logger_name):
        if logger_name != "":
            self._logger_name = "err.{0}".format(logger_name)
        else:
            raise ValueError("The given logger name is empty!")

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path=None):
        if file_path != "" or file_path is not None:
            self._file_path = file_path
        else:
            self._file_path = "/var/log/granary"

    def __init__(self, file_path, logger_name):
        file_formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        self.file_path = file_path
        self.logger_name = logger_name
        fully_path = "{file_path}/{filename}".format(
            file_path=self.file_path, filename="err.log"
        )
        log_handler = logging.handlers.RotatingFileHandler(
            fully_path, maxBytes=1048576, backupCount=5
        )
        log_handler.setFormatter(file_formatter)
        self._logger = logging.getLogger(self._logger_name)
        self._logger.setLevel(logging.WARNING)
        self._logger.addHandler(log_handler)

    def error(self, msg):
        self._logger.info(msg)
