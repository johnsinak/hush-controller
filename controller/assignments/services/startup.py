from assignments.models import Proxy
from assignments.services import poller_threads
import requests

def startup():
    if Proxy.objects.all().count() != 0:
        #Note: can be changed if needed
        print('database is already populated')
        return
    
    INSTANCE_INFO_URL = "http://44.197.203.24:8000/getInitDetails"

    response = requests.get(INSTANCE_INFO_URL)

    response_dict = dict(response.json())
    proxy_ip_list = []

    for key in response_dict.keys():
        proxy_ip_list.append(response_dict[key]['PublicIpAddress'])
    
    for ip in proxy_ip_list:
        Proxy.objects.create(ip=ip)

    poller_thread = poller_threads.PollerThread()
    poller_thread.start()

    #TODO: Add a system for migrations and stuff, since we don't have the push for the current test
