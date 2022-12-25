import time

from adapter import DBAdapter
from helpers.utils import read_config, get_handler


def main():
    start_time = time.time()

    db_config = read_config()
    db_type = db_config.get("db")

    DBHandler = get_handler(db_type)(**db_config)
    db_adapter = DBAdapter(DBHandler)
    db_adapter.connect().insert_data().close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    # Print the elapsed time
    print(f"Time consumed: {elapsed_time:.6f} seconds")


if __name__ == "__main__":
    main()
