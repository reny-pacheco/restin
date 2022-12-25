from typing import Union
from handlers.postgres import Postgres
from handlers.mongo import MongoDB


class DBAdapter:
    def __init__(self, cls: Union[Postgres, MongoDB]):
        self.cls = cls

    def connect(self):
        self.cls.connect()
        return self.cls

    def insert_data(self):
        self.cls.insert_data()
        return self.cls

    def close(self):
        self.cls.close()
