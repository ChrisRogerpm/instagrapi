from decouple import config
import mysql.connector


class Database:
    def __init__(self):
        self.config = {
            'host': config('MYSQL_HOST'),
            'user': config('MYSQL_USER'),
            'password': config('MYSQL_PASSWORD'),
            'database': config('MYSQL_DB'),
            'port': config('MYSQL_PORT'),
            'raise_on_warnings': True,
            'autocommit': True
        }

    def __enter__(self):
        self.cnx = mysql.connector.connect(**self.config)
        return self.cnx.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.commit()
        self.cnx.close()

    def saveOrUpdate(self, query, parameters):
         with self as cursor:
            cursor.execute(query, parameters)
            return True

    def get(self, query, parameters=None):
        with self as cursor:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result