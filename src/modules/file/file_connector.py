import pydantic
from typing import Tuple
from data_handler import data_object
from loguru import logger
from IO_file import remove_db_file, db_initiated_check


def read_header() -> Tuple[float, float]:
    # reads hours overhang initial and hours overhang left
    #returns 
    return


def store_header():
    # reads hours overhang initial and hours overhang left
    return


def read_body():
    # reads the data entries scraping of time
    return


def read_body() -> list(data_object):
    # reads the data entries scraping of time
    return


def is_initiated(path) -> bool:
    # check if db is present
    db_initiated_check(path)
    return False

def purge_db(path) -> Tuple[bool, Exception]:
    return remove_db_file(path)

