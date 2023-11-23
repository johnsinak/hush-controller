import sqlite3
from sqlite3 import Error
from settings import DATABASE_PATH
from queries import *

class DAO:
    def __init__(self, database_path=None) -> None:
        """init the connection to the database"""
        if database_path:
            self.database_path = database_path
        else:
            self.database_path = DATABASE_PATH

        try: 
            self.connection = sqlite3.connect(self.database_path)
            print(f"Database {self.database_path} formed.") 
        except Error as e:
            print(f"The error '{e}' occurred with the database")
            exit(1)
        
        self.__init_database__()

    def __execute_query__(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def __init_database__(self):
        self.__execute_query__(PROXIES_TABLE_CREATION_QUERY)
        self.__execute_query__(CLIENTS_TABLE_CREATION_QUERY)
        self.__execute_query__(CONNECTIONS_TABLE_CREATION_QUERY)

    def add_proxy(self, proxy):
        #TODO:
        pass

    def add_client(self, client):
        #TODO:
        pass