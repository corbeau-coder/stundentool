from loguru import logger
import os
import sys
import sqlite3
from typing import Tuple, List, Optional
from modules.data.data_handler import data_object, header_object


class DatabaseHandler:
    def __init__(self, conn):
        logger.debug(f"initializing DatabaseHandler with conn {conn}")
        self.db_initiated = False
        self._conn = None

        if conn is None:
            logger.error(f"Aborting initialization, conn variable is None {conn}")
        else:
            self._conn = conn
            try:
                resp = self._conn.cursor().execute("SELECT value FROM header")
                if (sum(1 for e in resp)) == 1:
                    self.db_initiated = True
                else:
                    logger.debug(
                        f"DB not properly initiated. Expected one row in header table, got this response: {resp}"
                    )
                    self.db_initiated = False
            except sqlite3.OperationalError as e:
                self.db_initiated = False
                logger.debug(f"DB connection cannot be established - Exception {str(e)}")
    

    def init_db(self, hours_initial: float) -> Tuple[bool, str]:
        logger.info("Initating database ...")
        sql_strings = [
            "CREATE TABLE header (value float NOT NULL)",
            "CREATE TABLE body (date DATE NOT NULL , hours float NOT NULL)",
        ]
        if self._conn is None:
            logger.debug("Aborting init, _conn is None")
            return (False, "database connection is None, aborting.")

        if self.db_initiated:
            logger.debug("Aborting init, db_initiated is True")
            return (
                False,
                "Database already initiated, aborting. Use purge function first if you want to reset database",
            )
        else:
            try:
                cursor = self._conn.cursor()
                for item in sql_strings:
                    res = cursor.execute(item)
                    if res.fetchone is None:
                        logger.error(f"ERROR executing SQL command\n{item}")
                        raise sqlite3.OperationalError
                cursor.execute(
                    "INSERT INTO header (value) VALUES (?)", (hours_initial,)
                )
                self._conn.commit()
            except sqlite3.OperationalError as e:
                logger.error(f"ERROR connecting database and creating tables {e}")
                return False, str(e)

            logger.info(" done.")
            return True, ""

    def read_all(self) -> Optional[List[data_object]]:
        logger.info("Reading all items from database ...")
        sql_string = "SELECT * FROM body"

        if not self.HealthCheck():
            return None
        else:
            try:            
                cursor = self._conn.cursor()
                res = cursor.execute(sql_string)
                self._conn.row_factory = self.data_object_factory
                ret_data = res.fetchall()
            except sqlite3.OperationalError as e:
                logger.error(f"Error {e} while executing sql_string {sql_string}")
                sys.exit(1)
            return ret_data

    def read_one(self, id) -> Optional[data_object]:
        logger.info(f"Reading item with ID {id} from database ...")
        sql_string = f"SELECT * FROM body WHERE ROWID is {id}"

        if not self.HealthCheck():
            return None
        else:
            try:
                cursor = self._conn.cursor()
                res = cursor.execute(sql_string)
                self._conn.row_factory = self.data_object_factory(cursor)
                ret_data = res.fetchone()
                if ret_data is None:
                    logger.error(f"cannot read item with id {id}")
                    sys.exit(1)
                else:
                    logger.info("done")
                    return ret_data
            except sqlite3.OperationalError as e:
                logger.error(f"failed\nError {e} while executing sql_string {sql_string}")

    def read_header(self) -> Optional[header_object]:
        logger.info(f"Reading header from database ...")
        sql_string = f"SELECT * FROM header"

        if not self.HealthCheck():
            return None
        else:
            try:
                cursor = self._conn.cursor()
                res = cursor.execute(sql_string)
                ret_data = res.fetchone()
                logger.debug(f"received following row from header select: {ret_data}")
                if ret_data is None:
                    logger.error(f"cannot read header")
                    return None
                else:
                    logger.info("done")
                    return header_object(ret_data[0])
            except sqlite3.OperationalError as e:
                logger.error(f"failed\nError {e} while executing sql_string {sql_string}")

            
    def write_one(self, data: data_object):
        logger.info("Writing new item into database ...")
        sql_string = "INSERT INTO body (date, hours) VALUES (?,?)"

        if not self.HealthCheck():
            return
        else:
            try:   
                cursor = self._conn.cursor()
                last_row_id = cursor.lastrowid
                if last_row_id is None:
                    last_row_id = 0
                cursor.execute(sql_string, (data.timestamp, data.hours))
                self._conn.commit()
            except sqlite3.OperationalError as e:
                logger.error(f"failed. Exception {e}")
                sys.exit(1)

            cur_last_row_id = cursor.lastrowid
            if cur_last_row_id is None or (cur_last_row_id <= last_row_id):
                logger.error(
                    f"failed. last row ids identical before and after insert: {last_row_id} {cur_last_row_id}"
                )
                sys.exit(1)
            else:
                logger.info(f"done.\nNew row added {cur_last_row_id} with data {data}")
                sys.exit(0)

    def delete_one(self, id) -> bool:
        logger.info(f"Deleting data item with ID {id}")
        sql_string = f"DELETE FROM body WHERE ROWID = {id}"

        if not self.HealthCheck():
            return False
        else:
            try:        
                cursor = self._conn.cursor()
                cursor.execute(sql_string)
            except sqlite3.OperationalError as e:
                logger.error(f"failed. Exception {e} occured while deleting row id {id}")
                return False
            logger.info(f"done.\nRow id {id} removed from dataset.")
            return True

    def data_object_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return data_object(**{k: v for k, v in zip(fields, row)})
    
    def HealthCheck(self) -> bool:
        if self._conn is None:
            logger.info("FAILED")
            logger.debug("Aborting, _conn is None")
            return False
        
        if not self.db_initiated:
            logger.info("FAILED")
            logger.debug("Aborting, DB not initiated")
            return False
        
        return True
