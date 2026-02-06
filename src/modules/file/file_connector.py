import pydantic
from typing import Tuple
from data_handler import data_object
from loguru import logger
from IO_file import remove_db_file


def read_header():
    # reads hours overhang initial and hours overhang left
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
    return False

def purge_db(path) -> Tuple[bool, Exception]:
    return remove_db_file(path)

