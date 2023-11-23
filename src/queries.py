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

CLIENTS_TABLE_CREATION_QUERY = """
            CREATE TABLE IF NOT EXISTS clients (
            ip TEXT PRIMARY KEY,
            first_request TEXT NOT NULL,
            request_count INTEGER NOT NULL
            );
            """

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