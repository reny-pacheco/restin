from typing import Dict, Tuple
import csv
from concurrent import futures

import psycopg2

from handlers.insert_base import InsertBase


InsertCommand = Tuple[str, Tuple[str, str]]
Data = Dict[str, str]


class Postgres(InsertBase):
    def __init__(self, **kwargs) -> None:
        from helpers.utils import validate_config

        validate_config(kwargs)
        self.dbname = kwargs.get("dbname")
        self.table_name = kwargs.get("tablename")
        self.filename = kwargs.get("filename")
        self.schema = kwargs.get("schema")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.cursor = None
        self.connection = None

    def connect(self) -> "Postgres":
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.connection = connection
            self.cursor = connection.cursor()
            return self
        except psycopg2.OperationalError:
            print("Error while connecting to DB")

    def insert_data(self) -> "Postgres":
        # create table if table doesn't exist
        self.__create_table()
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

            print("All data inserted")
            return self
        except FileNotFoundError as e:
            print("Error while inserting data")
            print(type(e))

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("DB connection closed.")

    # private methods
    def __create_table_command(self) -> str:
        from helpers.enums import Schema

        command = f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
        for (
            key,
            value,
        ) in self.schema.items():
            command += f"{key} {Schema[value].value},"
        return command[:-1] + ")"

    def __create_table(self):
        try:
            command = self.__create_table_command()
            self.cursor.execute(command)
            self.connection.commit()
            print("Table is now ready")
        except (
            AttributeError,
            psycopg2.ProgrammingError,
            psycopg2.OperationalError,
        ) as e:
            print(e)
            print("Error while creating table")

    def __create_insert_command(self, data: Data) -> InsertCommand:
        command = f"INSERT INTO {self.table_name}"
        col = "("
        row = "VALUES ("
        values = []

        for key, value in data.items():
            col += f"{key},"
            row += f"%s,"
            values.append(value)
        col = col[:-1] + ")"
        row = row[:-1] + ")"
        command = f"{command} {col} {row}"
        return command, tuple(values)

    def __insert(self, data):
        try:
            self.__serialize(data)
            insert_command, values = self.__create_insert_command(data)
            self.cursor.execute(insert_command, values)
            self.connection.commit()
        except ValueError:
            print(f"Error while inserting data ==> {data}")

    def __serialize(self, data):
        for key, value in self.schema.items():
            if value in ["number", "decimal"]:
                data[key] = float(data[key])
        return data
