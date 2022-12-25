import json
from typing import Dict, Union

from helpers.enums import DB

from handlers.postgres import Postgres
from handlers.mongo import MongoDB


def read_config() -> Dict[str, str]:
    try:
        with open("config.json", "r") as file:
            json_string = file.read()
        return json.loads(json_string)
    except FileNotFoundError:
        print("config.json file not found")


def validate_config(args):
    """Validates class attributes for DB handlers

    Args:
        args (dict): attributes of a class from a config file

    Raises:
        ValueError: Raise ValueError if one of the values is empty
    """
    for key, value in args.items():
        if key in ["client", "connection"]:
            continue
        if not value:
            print(f">>> {key} cannot be empty")
            raise ValueError()


def get_handler(db: str) -> Union[Postgres, MongoDB]:
    try:
        return DB[db].value
    except KeyError:
        print(">>> Invalid DB type...")
