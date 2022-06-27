import psycopg2
import psycopg2.extras


class Database:
    connection = None

    def connect(self):
        try:
            if self.connection is None:
                self.connection = psycopg2.connect(
                    user='postgres',
                    password='password',
                    host='localhost',
                    port='5432',
                    database='twitter_db'
                )
        except psycopg2.DatabaseError as e:
            print("Unable to connect :/")
            raise e
        return self.connection

    def execute_statement(self, statement: str, values=None):
        """General statement execution for DB."""
        connection = self.connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if values:
            cursor.execute(statement, values)
        else:
            cursor.execute(statement)
        return cursor
