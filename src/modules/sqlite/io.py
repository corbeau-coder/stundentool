from loguru import logger
import os
import sqlite3

class ConnectionHandler:
    def __init__(self, path = None) -> None:
        if path is None:
            self.path = "stundentool.db"
        else:
            self.path = path
        
        if not os.path.isfile(self.path):
            logger.debug(f"DB file is not present at {self.path}")
            self.db_exists = False

        self.conn = sqlite3.
        return self.conn
    
    def purge() -> 