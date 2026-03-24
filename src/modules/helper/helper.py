from abc import ABC

class Result(ABC):
    pass

class Success(Result):
    def __init__(self, payload):
        self.payload = payload

class Failure(Result):
    def __init__(self, err_msg):
        self.err_msg = err_msg