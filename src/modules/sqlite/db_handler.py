from loguru import logger
from typing import Tuple, List
from modules.data.data_handler import data_object
from modules.sqlite.io import ConnectionHandler
from modules.sqlite.db import DatabaseHandler


class db_object:
    def __init__(self, path):
        self._path = path
        self._conn = None
        self._db_handle = None
        self._con_handle = None
        self._db_file_present = False
        self._db_initiated = False
        if self._path is None:
            logger.error(f"Error initiating db_object, missing path {path}")
        else:
            self._con_handle = ConnectionHandler(self._path)
            self._db_file_present = self._con_handle.db_file_present
            if not self._db_file_present:
                logger.warning("WARN: db file not present")
            else:
                self._conn = self._con_handle.GetConnection()
                self._db_handle = DatabaseHandler(self._conn)
                self._db_initiated = self._db_handle.db_initiated
            return

    def purge_db(self) -> Tuple[bool, str]:
        if self._db_file_present:
            self._con_handle.CloseConnection()
            return self._con_handle.purge_db()
        else:
            return False, "db file not present"

    def init_db(self, hours_initial: float) -> Tuple[bool, str]:
        if not self._db_file_present:
            self._con_handle.create_db_file()
        self._conn = self._con_handle.GetConnection()
        self._db_handle = DatabaseHandler(self._conn)
        self._db_initiated = self._db_handle.db_initiated
        return self._db_handle.init_db(hours_initial)
        
    def read_all(self) -> List[data_object]:
        if self._db_file_present & self._db_initiated:
            return self._db_handle.read_all()
        else:
            logger.error("db not ready")
            return
        
    def read_one(self, id) -> data_object:
        if self._db_file_present & self._db_initiated:
            return self._db_handle.read_one(id)
        else:
            logger.error("db not ready")
            return

    def write_one(self, data: data_object):
        if self._db_file_present & self._db_initiated:
            return self._db_handle.write_one(data)
        else:
            logger.error("db not ready")
            return

    def delete_one(self, id) -> bool:
        if self._db_file_present & self._db_initiated:
            return self._db_handle.delete_one(id)
        else:
            logger.error("db not ready")
            return False