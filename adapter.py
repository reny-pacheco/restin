from handlers.postgres import Postgres


class DBAdapter:
    def __init__(self, cls: Postgres):
        self.cls = cls

    def connect(self):
        self.cls.connect()
        return self.cls

    def create_table(self):
        self.cls.create_table()
        return self.cls

    def insert_data(self):
        self.cls.insert_data()
        return self.cls

    def close(self):
        self.cls.close()
