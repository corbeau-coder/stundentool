from src.modules.sqlite.db_handler import db_object
from typing import Tuple, List, Optional
from modules.data.data_handler import data_object, header_object


class store_handler():
    def __init__(self, path):
        self.db_obj = db_object(path)

    def db_status(self) -> bool:
        return self.db_obj.GetDBStatus()

    def purge(self, path) -> Tuple[bool, str]:
        return self.db_obj.purge_db()
        
    def init(self, hours_initial: float):
        self.db_obj.init_db(hours_initial)
        return
    
    def read_all(self) -> Optional[List[data_object]]:
        return self.db_obj.read_all()
    
    def read_one(self, id) -> Optional[data_object]:
        return self.db_obj.read_one(id)
    
    def write_one(self, data: data_object):
        return self.db_obj.write_one(data)
    
    def delete_one(self, id) -> bool:
        return self.db_obj.delete_one(id)
    
    def read_header(self) -> Optional[header_object]:
        return self.db_obj.read_header()
    
    def calc(self, data_items: List[data_object]) -> Tuple[float, float]:
        hours_sum = 0
        hours_initiated = self.read_header()
        if hours_initiated is None:
            return 0, 0
        else:
            for item in data_items:
                hours_sum += item.hours
            return hours_initiated.hours, hours_sum
        
