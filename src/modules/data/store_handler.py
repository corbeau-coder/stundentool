from loguru import logger
from pydantic import BaseModel
from modules.file.file_connector import is_initiated, purge_db
from typing import Tuple
from modules.data.data_handler import data_store


class store_handler(BaseModel):
    def __init__(self, path):
        self.db_initiated = is_initiated(path)

        if self.db_initiated:
            self.data_storage = data_store(path)

    def purge(self, path) -> Tuple[bool, Exception]:
        return purge_db(path)
        

    def init(self, hours_initial: float, path: str, *args, **kwargs):
        purge = kwargs.get("purge", False)
        if purge:
            result, e = self.purge(path)
        self.data_storage = data_store(path)
        return
