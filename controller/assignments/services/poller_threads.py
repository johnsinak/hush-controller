import threading
from time import sleep
import socket

from assignments.models import Proxy, ProxyReport


class PollerThread(threading.Thread):
    # def __init__(self, listen_endpoint: tuple, forward_endpoint: tuple):
    def __init__(self):
        threading.Thread.__init__(self)
        self.polling_frequency_mins = 5
        # self.forward_endpoint = forward_endpoint

    def run(self):
        polling_port = 8120
        try:
            while True:
                sleep(self.polling_frequency_mins * 60)
                active_proxies = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all()
                for proxy in active_proxies:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((proxy.ip, polling_port))
                    message = 'hello'
                    client_socket.send(message.encode('utf-8'))
                    data = client_socket.recv(8192)
                    client_socket.close()

                    # do the shit
                    #TODO:
                    ProxyReport.objects.create(proxy=proxy, utility = ,throughput= , connected_clients = ))
                    
        except Exception as e:
            print('ERROR: a fatal error has happened')
            print(e)