from loguru import logger
import os
import sys
import sqlite3
from typing import Tuple, List
from modules.data.data_handler import data_object


class db_object:
    def __init__(self, path):
        self._path = path
        self._conn = conn
        

    def purge_db(self) -> Tuple[bool, str]:
  

    def init_db(self, hours_initial: float) -> Tuple[bool, str]:
        
    def read_all(self) -> List[data_object]:
        
    def read_one(self, id) -> data_object:
        

    def write_one(self, data: data_object):
        

    def delete_one(self, id) -> bool:
        