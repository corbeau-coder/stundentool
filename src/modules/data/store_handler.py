from loguru import logger
from modules.sqlite.IO_db import db_object
from typing import Tuple, List
from modules.data.data_handler import data_object


class store_handler():
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
        return self.db_obj.read_all()
    
    def read_one(self, id) -> data_object:
        return self.db_obj.read_one(id)
    
    def write_one(self, data: data_object):
        return self.db_obj.write_one(data)
    
    def delete_one(self, id) -> bool:
        return self.db_obj.delete_one(id)
