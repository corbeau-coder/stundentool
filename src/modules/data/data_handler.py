
from loguru import logger

from datetime import datetime

class data_object():
    timestamp: datetime
    hours: float

    def __init__(self, hours: float):
        self.timestamp = datetime.now()
        self.hours = hours
        logger.debug(
            f"Created data object with following variable values:\ntimestamp: {self.timestamp}\nhours: {self.hours}\n"
        )