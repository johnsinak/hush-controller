from datetime import datetime

class ProxyModel:
    def __init__(self, url: str, created_at: datetime, utility=0.0, connected_users=0, avg_throughput=0.0, id = None) -> None:
        self.url = url
        self.created_at = created_at
        self.utility = utility
        self.connected_users = connected_users
        self.avg_throughput = avg_throughput
        self.id = id

    @classmethod
    def from_list(cls, value_list):
        # Additional constructor using only param1
        return cls(value_list[1], datetime.strptime(value_list[2], '%Y-%m-%d %H:%M:%S.%f'), value_list[3], value_list[4], value_list[5], value_list[0])


class ClientModel:
    def __init__(self, ip: str, first_request: datetime, request_count=0) -> None:
        self.ip = ip
        self.first_request = first_request
        self.request_count = request_count
    
    @classmethod
    def from_list(cls, value_list):
        # Additional constructor using only param1
        return cls(value_list[0], datetime.strptime(value_list[1], '%Y-%m-%d %H:%M:%S.%f'), value_list[2])
