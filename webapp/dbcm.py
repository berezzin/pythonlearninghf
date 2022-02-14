import mysql.connector as connector


class UseDatabase:
    def __init__(self, dbconfig: dict) -> None:
        self.dbconfig = dbconfig

    def __enter__(self) -> 'cursor':
        self.connection = connector.connect(**self.dbconfig)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
