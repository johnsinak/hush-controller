from time import sleep
import threading
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
    
    def poll_instance_manager(self):
        print('polled instance manager')
        #TODO:
        pass

    def poll_proxies(self):
        """ 
        get_proxy_list
        poll them
        update
        """
        print('polled proxies')

    def run(self):
        while (True):
            self.poll_instance_manager()
            self.poll_proxies()

            # TODO: Choose sleep duration
            sleep(10)

class PollerThread(threading.Thread):
    def __init__(self, poller: Poller):
        threading.Thread.__init__(self)
        self.poller = poller

    def run(self):
        try:
            self.poller.run()
        except Exception as e:
            print("CRITICAL ERROR: poller has died. message: ", repr(e))
