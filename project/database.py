from psycopg2 import pool


class Database:

    __connection_pool = None

    @classmethod
    def initialise(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        cls.__connection_pool.closeall()

class CursorFromConnectionPool:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value is not None:  # This is equivalent to `if exception_value is not None`
            self.conn.rollback()
        else:
            self.cursor.close()
            self.conn.commit()
        Database.return_connection(self.conn)
