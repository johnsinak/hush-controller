PROXIES_TABLE_CREATION_QUERY = """
            CREATE TABLE IF NOT EXISTS proxies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            created_at TEXT NOT NULL,
            utility REAL,
            connected_users INTEGER,
            avg_throughput REAL
            );
            """

PROXIES_INSERT_VALUES_QUERY = """
            INSERT INTO
                proxies (url, created_at, utility, connected_users, avg_throughput)
            VALUES
                ('{}', '{}', {}, {}, {});
            """

PROXIES_GET_ALL_VALUES = """SELECT * FROM proxies"""

CLIENTS_TABLE_CREATION_QUERY = """
            CREATE TABLE IF NOT EXISTS clients (
            ip TEXT PRIMARY KEY,
            first_request TEXT NOT NULL,
            request_count INTEGER NOT NULL
            );
            """

CLIENTS_INSERT_VALUES_QUERY = """
            INSERT INTO
                clients (ip, first_request, request_count)
            VALUES
                ('{}', '{}', {});
            """

CLIENTS_UPDATE_VALUES_QUERY = """
            UPDATE clients
            SET request_count = {}
            WHERE ip = '{}'
            """

CLIENTS_SEARCH_VALUES = """SELECT * FROM clients WHERE ip LIKE '{}'"""

CONNECTIONS_TABLE_CREATION_QUERY = """
            CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proxy_id INTEGER NOT NULL, 
            client_ip TEXT NOT NULL,
            request_time TEXT NOT NULL,
            is_active INTEGER,
            FOREIGN KEY (proxy_id) REFERENCES proxies (id) FOREIGN KEY (client_ip) REFERENCES clients (ip)
            );
            """

CONNECTIONS_INSERT_VALUES_QUERY = """
            INSERT INTO
                connections (proxy_id, client_ip, request_time, is_active)
            VALUES
                ({}, '{}', '{}', {});
            """