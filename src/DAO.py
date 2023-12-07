import sqlite3
from sqlite3 import Error
from settings import DATABASE_PATH
from queries import *
from models import *

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
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def __execute_search__(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"The error '{e}' occurred")

    def __init_database__(self):
        self.__execute_query__(PROXIES_TABLE_CREATION_QUERY)
        self.__execute_query__(CLIENTS_TABLE_CREATION_QUERY)
        self.__execute_query__(CONNECTIONS_TABLE_CREATION_QUERY)

    def add_proxy(self, proxy:ProxyModel):
        self.__execute_query__(PROXIES_INSERT_VALUES_QUERY.format(proxy.url, proxy.created_at, proxy.utility, proxy.connected_users, proxy.avg_throughput))

    def add_client(self, client:ClientModel):
        self.__execute_query__(CLIENTS_INSERT_VALUES_QUERY.format(client.ip, client.first_request, client.request_count))
        pass

    def find_client(self, ip) -> ClientModel:
        results = self.__execute_search__(CLIENTS_SEARCH_VALUES.format(ip))
        if results:
            return ClientModel.from_list(results[0])
        else:
            return None

    def add_connection(self, proxy:ProxyModel, client:ClientModel):
        pass
