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
    
    def purge_db(self) -> Tuple[bool, str]:
        logger.debug(f"IO module deleting db at {self.path}")
        try:
            os.remove(self.path)
        except FileNotFoundError as e:
            logger.debug(f"FAILED: {e}")
            return False, str(e)
        else:
            logger.debug("DONE")
            return True, ""
        
    self.path = path
        if not os.path.isfile(self.path):
            logger.debug(f"DB path is not a file {self.path}")
            self.db_exists = False
        else:
            sql_string = "SELECT value FROM header"
            try:
                with sqlite3.connect(self.path) as conn:
                    ret = conn.cursor().execute(sql_string).fetchone()
                    if ret is not None:
                        self.hours_initiated = ret
                        self.db_exists = True
                    else:
                        self.db_exists = False