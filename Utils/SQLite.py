import sqlite3
  
class SQLite():

    SEPARATOR:str = " : "
    DECODERS:dict[str, type] = {
        int.__name__: int,
        float.__name__: float,
        str.__name__: str,
        bool.__name__: eval,
        dict.__name__: eval,
        list.__name__: eval,
        tuple.__name__: eval,
        set.__name__: eval
    }
    sqlite_connection:sqlite3.Connection = None
    cursor:sqlite3.Cursor = None

    def __init__(self, path:str) -> None:
        self.sqlite_connection = sqlite3.connect(path)
        self.cursor = self.sqlite_connection.cursor()

    def __del__(self) -> None:
        if all((self.sqlite_connection, self.cursor)):
            self.close()

    def close(self) -> None:
        if self.cursor.execute("SELECT changes()").fetchone()[0]:
            self.sqlite_connection.commit()
        self.cursor.close()
        self.sqlite_connection.close()
        self.sqlite_connection = self.cursor = None

    @staticmethod
    def to_table(value:"Any") -> str:
        if ((type_name := type(value).__name__) in SQLite.DECODERS) or value is None:
            return f"{value}{SQLite.SEPARATOR}{type_name}"
        return SQLite.to_table(None)
    
    @staticmethod
    def from_table(record:str) -> "Any":
        if SQLite.SEPARATOR in record:
            value, annotation = (lambda args: reversed((args.pop(), str().join(args))))(record.split(SQLite.SEPARATOR))
            if decoder := SQLite.DECODERS.get(annotation):
                return decoder(value)
        return None
    
    def __getter(self) -> "yield":
        while records := self.cursor.fetchmany(1):
            yield records
    
    def execute(self, *args, **kwargs) -> None:
        return self.cursor.execute(*args, **kwargs)

    def get_table_names(self) -> "yield":
        self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
        for args in self.__getter():
            yield args[0][0]
    
    def get_table_column_names(self, table_name:str) -> "yield":
        self.execute(f"PRAGMA table_info({table_name})")
        for args in self.__getter():
            yield args[0][1]

    def get_table_primary_key_columns(self, table_name:str) -> "yield":
        self.execute(f"PRAGMA table_info({table_name})")
        for args in self.__getter():
            if args[0][5]:
                yield args[0][1]

    def get_table_params(self, table_name:str) -> "yield":
        self.execute(f"SELECT * FROM {table_name}")
        for args in self.__getter():
            yield map(SQLite.from_table, args[0])

    def get_table_data(self, table_name:str) -> "yield":
        table_columns = tuple(self.get_table_column_names(table_name))
        for data in self.get_table_params(table_name):
            yield zip(table_columns, tuple(data))

    def get_all_data(self) -> "yield":
        for table_name in tuple(self.get_table_names()):
            yield (table_name, self.get_table_data(table_name))

    def get_records(self, table_name:str, column:str, value:"Any") -> "yield":
        self.execute(f"SELECT * FROM {table_name} WHERE {column} = ?", (SQLite.to_table(value),))
        for args in self.__getter():
            yield map(SQLite.from_table, args[0])

    def update_records(self, table_name:str, column:str, value:"Any", where_column:str, where_value:"Any") -> None:
        self.execute(f"UPDATE {table_name} SET {column} = ? WHERE {where_column} = ?", (SQLite.to_table(value), SQLite.to_table(where_value)))

    def delete_records(self, table_name:str, column:str, value:str) -> None:
        self.execute(f"DELETE FROM {table_name} WHERE {column} = ?", (SQLite.to_table(value),))

    def create_table(self, table_name:str, table_columns:"Iterable") -> None:
        self.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(table_columns)})")

    def add_to_table(self, table_name:str, value:dict[str, "Any"]) -> None:
        try:
            self.execute(f"INSERT INTO {table_name} VALUES ({','.join('?' * len(params := tuple(map(lambda key: SQLite.to_table(value.get(key)), tuple(value.keys())))))})", params)
        except sqlite3.OperationalError as db_ex:
            if "no such table" in str(db_ex):
                self.create_table(table_name, tuple(value.keys()))
                return self.add_to_table(table_name, value)
            else: print(db_ex)

    def clear_table(self, table_name:str):
        self.execute(f"DELETE FROM {table_name}")

    def delete_table(self, table_name:str):
        self.execute(f"DROP TABLE {table_name}")

    def delete_table_column(self, table_name:str, column:str):
        self.execute(f"ALTER TABLE {table_name} DROP COLUMN {column}")

    def add_column_to_table(self, table_name:str, colunm:str, default:"Any" = None):
        self.execute(f"ALTER TABLE {table_name} ADD COLUMN {colunm}")
        self.execute(f"UPDATE {table_name} SET {colunm} = ?", (SQLite.to_table(default),))