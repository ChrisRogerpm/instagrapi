from decouple import config
import mysql.connector


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DB'),
            port=config('MYSQL_PORT'),
        )

    def saveOrUpdate(self, query, parameters):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()
        cursor.close()
        return True

    def get(self, query, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_transaction(self, queries):
        cursor = self.connection.cursor()
        try:
            for query in queries:
                cursor.execute(query['query'], query['parameters'])
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            cursor.close()
            return False
