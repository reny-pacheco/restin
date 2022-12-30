## restin

### An automation tool for inserting data to database from a csv file.

Currently compatible with Postgres and MongoDB.

### How to use?

Set up your Postgres or MongoDB database and update `config.json` file based on your db configuration.

### Example:

**Postgres config**

```json
{
  "db": "postgres",
  "dbname": "mydatabase",
  "user": "myuser",
  "password": "mypassword",
  "host": "localhost",
  "tablename": "users",
  "filename": "data.csv",
  "port": "5432",
  "schema": {
    "name": "string",
    "age": "number",
    "location": "string",
    "average": "decimal",
    "subject": "string"
  }
}
```

**MongoDB config**

```json
{
  "db": "mongodb",
  "dbname": "mydatabase",
  "collection": "users",
  "user": "myuser",
  "password": "mypassword",
  "host": "mongodb://localhost:27017/",
  "tablename": "users",
  "filename": "data.csv",
  "schema": {
    "name": "string",
    "age": "number",
    "location": "string",
    "average": "decimal",
    "subject": "string"
  }
}
```

**Notes:**

- `db` is the type of database you are using, e.g. postgres or mongodb.
- `filename` should be in the current project directory.
- `schema` should based on your csv headers. Keys are your column names and values are your data types. Currently, `string`, `text`, `number`, and `decimal` are the supported data types.

| Schema type | SQL Data type |
| ----------- | ------------- |
| string      | VARCHAR(255)  |
| number      | INTEGER       |
| decimal     | FLOAT         |
| text        | TEXT          |

For running the app use this command

- `python main.py`

**Todos**

- Add support for MySql
- Improve logging
- Add test
- Add web user interface
