from typing import Optional, Tuple
from loguru import logger
import os
import sqlite3
from modules.helper.helper import Result, Success, Failure

class ConnectionHandler:
    def __init__(self, path=None) -> None:
        self.db_file_present = False
        self._conn = None

        if path is None:
            self.path = "stundentool.db"
        else:
            self.path = path

        if not os.path.isfile(self.path):
            self.db_file_present = False
            logger.debug(f"DB file is not present at {self.path}")
            logger.error("db file missing, please use --init to create the database")
        else:
            self.db_file_present = True
            logger.debug("opening new connection, returning it")
            try:
                self._conn = sqlite3.connect(self.path)
            except sqlite3.OperationalError as e:
                logger.debug(f"error opening new connection. Exception {e}")
                self._conn = None

    def GetConnection(self) -> Optional[sqlite3.Connection]:
        logger.debug(f"GetConnection debug output: {self.db_file_present} {self._conn}")
        if self.db_file_present:
            if self._conn is None:
                self._conn = sqlite3.connect(self.path)
            return self._conn
        else:
            return None

    def CloseConnection(self) -> None:
        if self.db_file_present:
            if self._conn is None:
                logger.debug("self._conn is None, aborting CloseConnection")
                return
            else:
                try:
                    self._conn.commit()
                    self._conn.close()
                except sqlite3.OperationalError as e:
                    logger.debug(f"Error while closing connection. Exception {e}")
                    return
                logger.debug("CloseConnection successfull")
                return
        else:
            logger.debug("self.db_file_present is False, aborting CloseConnection")
            return

    def purge_db(self) -> Result:
        logger.debug(f"IO module deleting db at {self.path}")
        if self.db_file_present and self._conn is not None:
            try:
                self._conn.commit()
                self._conn.close()
            except sqlite3.OperationalError as e:
                logger.debug(f"FAILED. Closing DB went wrong. Exception {e}")

        self.db_file_present = False
        try:
            os.remove(self.path)
        except FileNotFoundError as e:
            logger.debug(f"FAILED. Deleting file went wrong. Exception {e}")
            return Failure(str(e))
        else:
            logger.debug("DONE")
            return Success("")

    def create_db_file(self) -> Result:
        logger.debug(f"creating db file at {self.path}")
        if self.db_file_present:
            logger.debug("FAILED. Aborting while file_present flag is set")
            return Failure(
                "db_file_present flag is True, iniating is forbidden. If you want to initiate anyway, please purge db before this step.",
            )
        else:
            if not os.path.exists(self.path):
                open(self.path, "a").close()
                logger.debug("DONE")
                self.db_file_present = True
                return Success("")
            else:
                logger.debug("FAILED")
                return Failure(f"file exists, aborting file creation at {self.path}")
