from enum import Enum

from handlers.postgres import Postgres


class Schema(Enum):
    string = "VARCHAR(255)"
    number = "INTEGER"
    decimal = "FLOAT"
    text = "TEXT"


class DB(Enum):
    postgres = Postgres
