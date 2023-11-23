
class Poller:
    def __init__(self, intance_manager_address, proxy_list=[]) -> None:
        """
        endpoints are tuples of: (address, port)
        """
        self.intance_manager_address = intance_manager_address
        self.__add_proxies_to_database__(proxy_list)

    def __add_proxies_to_database__(self, proxy_list):
        for proxy in proxy_list:
            #TODO:
            pass