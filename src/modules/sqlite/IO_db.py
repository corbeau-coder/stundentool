from loguru import logger
import os
import sys
import sqlite3
from typing import Tuple, List
from modules.data.data_handler import data_object


class db_object:
    def __init__(self, path):
        self.path = path
        if not os.path.isfile(self.path):
            logger.debug(f"DB path is not a file {self.path}")
            self.db_exists = False
        else:
            self.db_exists = True

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

    def init_db(self, hours_initial: float) -> Tuple[bool, str]:
        logger.info("Initating database ...")
        sql_strings = [
            "CREATE TABLE header (value float NOT NULL)",
            "CREATE TABLE body (date DATE NOT NULL , hours float NOT NULL)",
        ]
        try:
            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                for item in sql_strings:
                    res = cursor.execute(item)
                    if res.fetchone is None:
                        logger.error(f"ERROR executing SQL command\n{item}")
                        raise sqlite3.OperationalError
                cursor.execute("INSERT INTO header (value) VALUES (?)", (hours_initial,))
        except sqlite3.OperationalError as e:
            logger.error(
                f"ERROR connecting database and creating tables {self.path} {e}"
            )
            #TODO die Tabellen müssen gedropt werden
            return False, str(e)

        logger.info(" done.")
        return True, ""

    def read_all(self) -> List[data_object]:
        logger.info("Reading all items from database ...")
        sql_string = "SELECT * FROM body"

        try:
            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                res = cursor.execute(sql_string)
                conn.row_factory = self.data_object_factory
                ret_data = res.fetchall()
        except sqlite3.OperationalError as e:
            logger.error(f"Error {e} while executing sql_string {sql_string}")
            sys.exit(1)
        return ret_data

    def read_one(self, id) -> data_object:
        logger.info(f"Reading item with ID {id} from database ...")
        sql_string = f"SELECT * FROM body WHERE ROWID is {id}"

        try:
            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                res = cursor.execute(sql_string)
                conn.row_factory = self.data_object_factory
                ret_data = res.fetchone()
                if (ret_data is None):
                    logger.error(f"cannot read item with id {id}")
                    sys.exit(1)
        except sqlite3.OperationalError as e:
            logger.error(f"failed\nError {e} while executing sql_string {sql_string}")

        logger.info("done")
        return ret_data

    def write_one(self, data: data_object):
        logger.info("Writing new item into database ...")
        sql_string = "INSERT INTO body (date, hours) VALUES (?,?)"

        try:
            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                last_row_id = cursor.lastrowid
                if last_row_id is None:
                    last_row_id = 0
                cursor.execute(sql_string, (data.timestamp, data.hours))
                conn.commit()
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

        try:
            with sqlite3.connect(self.path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_string)
        except sqlite3.OperationalError as e:
            logger.error(f"failed. Exception {e} occured while deleting row id {id}")
            return False
        logger.info(f"done.\nRow id {id} removed from dataset.")
        return True

    def data_object_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return data_object(**{k: v for k, v in zip(fields, row)})
