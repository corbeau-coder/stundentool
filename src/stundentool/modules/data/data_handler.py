from pydantic import BaseModel, datetime

class hour_surge(BaseModel):
    timestamp: datetime
    hours: float

    def __init__(hours: float) -> 

class data_store(BaseModel):
    hours_overhang_initial: int
    hours_overhang_left: int
    entries_hours_surged: list
