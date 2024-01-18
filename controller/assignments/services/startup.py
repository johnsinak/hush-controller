from assignments.models import Proxy
from assignments.services import poller_threads
import requests

def startup():
    if Proxy.objects.all().count() != 0:
        #TODO: can be changed if needed
        print('database is already populated')
        return
    
    INSTANCE_INFO_URL = "http://44.197.203.24:8000/getInitDetails"

    response = requests.get(INSTANCE_INFO_URL)
    
    #TODO: somehow create into a list
    proxy_ip_list = response.json()
    
    for ip in proxy_ip_list:
        Proxy.objects.create(ip=ip)

    poller_thread = poller_threads.PollerThread()
    poller_thread.start()
