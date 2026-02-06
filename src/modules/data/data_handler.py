import sys

from pydantic import BaseModel

from loguru import logger

import datetime as datetime
from file.file_connector import is_initiated, purge_db, read_header


class data_object(BaseModel):
    timestamp: datetime.datetime
    hours: float

    def __init__(self, hours: float):
        self.timestamp = datetime.datetime.now()
        self.hours = hours
        logger.debug(
            "Created data object with following variable values:\nttimestamp: {self.timestamp}\nhours: {self.hours}\n"
        )


class data_store(BaseModel):
    hours_overhang_initial: float
    hours_overhang_left: float
    entries_hours_surged: list
    path: str

    def __init__(self, *args, **kwargs):
        self.path = "stunden.db"
        hours_overhang_initial = kwargs.get("hours_initial", None)
        do_purge = kwargs.get("purge_db", False)
        

        if do_purge:
            return
        if init:
        elif is_initiated(self.path):
            hours_overhang_initial, hours_overhang_left = read_header(self.path)
        elif not (isinstance(hours_overhang_initial, float) and not is_initiated(self.path)):
            logger.error(
                "Error initializing database, argument for initial hour overhang is not from type float"
            )
            raise TypeError("wrong parameter type")
             

        self.hours_overhang_initial = hours_overhang_initial
        self.hours_overhang_left = hours_overhang_initial

        return

    def delete_db(self):
        try:
            purge_db(self.path)
        except FileNotFoundError as e:
            logger.error("Error deleting db, file not found {e}")
            sys.exit(1)
        except OSError as e:
            logger.error("Error deleting db, IOError {e}")
            sys.exit(1)
        return 

    def add_item(self, hours: float):
        self.store_body(data_object(hours))
        return

    def read_item(self, index: int) -> data_object:
        return None

    def read_time_stats(self) -> tuple[float, float]:
        return self.hours_overhang_initial, self.hours_overhang_left

    def read_body(self) -> list[data_object]:
        return None

    def store_body(self, data: data_object):
        file_content_body = self.read_body()
        file_content_body.append(data)
        # IO store body
        return

    def read_header(self):
        # write header (self.hours_overhang_inital, self.hours_overhang_left)
        return

    def store_header(self):
        # write header (self.hours_overhang_inital, self.hours_overhang_left)
        return

    def calculate_time_left(self, *args, **kwargs):
        check_for_reinitiation = kwargs.get("re_init", False)
        hours_delta = kwargs.get("hours", None)

        if check_for_reinitiation:
            logger.debug("Re-Initiation of calculated time left is requested.")
            hours_delta = 0
            object_list = self.read_body()
            for item in object_list:
                hours_delta += item.hours
            logger.debug(
                "Summed up {hours_delta} hours already reported as scraped off"
            )
            self.hours_overhang_left = self.hours_overhang_initial
        else:
            if hours_delta is None:
                logger.debug(
                    "Error while calculation, value of hours_delta is None {hours_delta}"
                )
                raise (ValueError("Error: calculation value is empty {hours_delta}"))

        logger.debug("Calculating hours left {self.hours_overhang_left} {hours_delta}")
        self.hours_overhang_left = self.hours_overhang_left - float(hours_delta)

        return
