from client_manager import client_manager_server
from DAO import DAO
from models import *
from poller import *
from settings import *

if __name__ == "__main__":
    poller = Poller(INSTANCE_MANAGER_ADDRESS)
    poller_thread = PollerThread(poller)
    poller_thread.start()

    client_manager_server()
    