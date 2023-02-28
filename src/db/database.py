import mysql.connector
import os


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            port=os.getenv("MYSQL_PORT"),
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
