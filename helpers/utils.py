import json

from helpers.enums import DB

from handlers.postgres import Postgres


def read_config():
    try:
        with open("config.json", "r") as file:
            json_string = file.read()
        return json.loads(json_string)
    except FileNotFoundError:
        print("config.json file not found")


def get_handler(db) -> Postgres:
    try:
        return DB[db].value
    except KeyError:
        print(">>> Invalid DB type...")
