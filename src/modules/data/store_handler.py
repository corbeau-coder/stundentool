from loguru import logger
from pydantic import BaseModel
from modules.sqlite.IO_db import db_object
from typing import Tuple, List
from modules.data.data_handler import data_object


class store_handler(BaseModel):
    def __init__(self, path):
        self.db_obj = db_object(path)

    def db_status(self) -> bool:
        return self.db_obj.db_exists

    def purge(self, path) -> Tuple[bool, str]:
        return self.db_obj.purge_db()
        
    def init(self, hours_initial: float):
        self.db_obj.init_db(hours_initial)
        return
    
    def read_all(self) -> List[data_object]:
        self.db_obj.
