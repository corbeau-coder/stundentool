from pydantic import BaseModel

from loguru import logger

import datetime as datetime


def graduation_checker(value_to_check: float):
    if not (isinstance(value_to_check, float)):
        logger.error(f"Error handling hour input {value_to_check}: wrong input type")
        raise TypeError("Error: input has wrong type, expected float ( 12.34 )")
    elif not (value_to_check % .25 == 0): 
        logger.error(f"Error handling hour input {value_to_check}: valid float but invalid graduated")
        raise ValueError("Error: Value given is not chosen correctly")
    else:
        return
        

class data_object(BaseModel):
    timestamp: datetime.datetime
    hours: float

    

    def __init__(self, hours: float) -> tuple[bool, Exception]:
        try:
            graduation_checker(hours)
        except Exception as e:
            logger.error(f"Error initiating the data object\ninput value: {hours}")
            raise e
        else:
            self.timestamp = datetime.datetime.now()
            self.hours = hours
            logger.debug("Created data object with following variable values:\nttimestamp: {self.timestamp}\nhours: {self.hours}\n")
            return (True, None)

class data_store(BaseModel):
    hours_overhang_initial: int
    hours_overhang_left: int
    entries_hours_surged: list

    def __init__(self, *args, **kwargs):
        hours_overhang_initial = kwargs.get("hours_initial", None)
        do_purge = kwargs.get("purge_db", False)
       
        if not (isinstance(hours_overhang_initial, float)):
            logger.error("Error initializing database, argument for initial hour overhang is not from type float")
            raise TypeError("wrong parameter type")
        elif do_purge:
            try:
                self.delete_db()
            except OSError as e:
                logger.error("Error deleting db, IOError {e}")
                raise e
            except FileNotFoundError as  e:
                logger.error("Error deleting db, file not found {e}")
                raise e



        self.hours_overhang_initial = hours_overhang_initial
        self.hours_overhang_left = hours_overhang_initial
        return
    

    
    def delete_db():
        return

    def add_item(self, hours: float):
        self.store_data(data_object(hours))
        return
    
    def read_item(self, index: int) -> data_object:
        return None
      
    def read_time_stats(self) -> tuple [float, float]:
        return self.hours_overhang_initial, self.hours_overhang_left
    
    def read_data(self) -> list[data_object]:
        return None

    def store_data(self, data: data_object):
        file_content_body = self.read_data()
        file_content_body.append(data)
        #IO store body
        return

    def read_header():
        #write header (self.hours_overhang_inital, self.hours_overhang_left)
        return

    def store_header():
        #write header (self.hours_overhang_inital, self.hours_overhang_left)
        return

    def calculate_time_left(self, *args, **kwargs):
        check_for_reinitiation = kwargs.get("re_init", False)
        hours_delta = kwargs.get("hours", None)

        if check_for_reinitiation:
            logger.debug("Re-Initiation of calculated time left is requested.")
            hours_delta = 0
            object_list = self.read_all_items
            for item in object_list:
                hours_delta += item.hours
            logger.debug("Summed up {hours_delta} hours already reported as scraped off")
            self.hours_overhang_left = self.hours_overhang_initial


        logger.debug("Calculating hours left {self.hours_overhang_left} {hours_delta}")
        self.hours_overhang_left = self.hours_overhang_left - hours_delta

        return




