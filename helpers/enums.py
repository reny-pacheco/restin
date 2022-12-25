from enum import Enum

from handlers.postgres import Postgres
from handlers.mongo import MongoDB


class Schema(Enum):
    string = "VARCHAR(255)"
    number = "INTEGER"
    decimal = "FLOAT"
    text = "TEXT"


class DB(Enum):
    postgres = Postgres
    mongodb = MongoDB
