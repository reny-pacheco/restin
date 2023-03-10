from typing import Dict
import csv
from concurrent import futures

from pymongo import MongoClient, errors

from handlers.insert_base import InsertBase

Data = Dict[str, str]


class MongoDB(InsertBase):
    def __init__(self, **kwargs) -> None:
        from helpers.utils import validate_config

        validate_config(kwargs)
        self.dbname = kwargs.get("dbname")
        self.collection = kwargs.get("collection")
        self.schema = kwargs.get("schema")
        self.filename = kwargs.get("filename")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.host = kwargs.get("host")
        self.client = None

    def connect(self) -> "MongoDB":
        try:
            client = MongoClient(
                host=self.host, username=self.user, password=self.password
            )
            self.client = client
            return self
        except errors.OperationFailure:
            print("Error while connecting to DB")

    def insert_data(self) -> "MongoDB":
        print("Inserting data...")

        try:
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)
                MAX_THREADS = 5

                with futures.ThreadPoolExecutor(
                    max_workers=MAX_THREADS
                ) as executor:
                    for data in reader:
                        executor.submit(self.__insert, data)

            print("Data insertion has been completed")
            return self
        except FileNotFoundError:
            print("Error while inserting data")

    def close(self):
        self.client.close()
        print("DB connection closed.")

    def __insert(self, data):
        try:
            db = self.client[self.dbname]
            collection = db[self.collection]
            data = self.__serialize(data)
            collection.insert_one(data)
        except ValueError:
            print(f"Error while inserting data ==> {data}")

    def __serialize(self, data):
        for key, value in self.schema.items():
            if value in ["number", "decimal"]:
                data[key] = float(data[key])
        return data
