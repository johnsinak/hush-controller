from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from assignments.services.startup import id_to_nums
from scripts.config_basic import CENSORED_REGION_SIZE
from random import randint
from time import time
from assignments.models import *

def calcualte_distance(point_1, point_2):
    return ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5

def get_normalized_distance(point_1, point_2):
    return calcualte_distance(point_1, point_2) / CENSORED_REGION_SIZE


def request_new_proxy(user_ip):
    try:
        client = Client.objects.get(ip=user_ip)
    except ObjectDoesNotExist:
        client = Client.objects.create(ip=user_ip, user_agent="LemonadeOS device")
        # O1: provide with random proxy and done. discuss this
        # active_proxies = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all()
        # chosen_proxy = active_proxies[randint(0,len(active_proxies) - 1)]

        # O2: provide with random proxy and done. discuss this
        chosen_proxy = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all().first()

        Assignment.objects.create(proxy=chosen_proxy, client=client)
        chosen_proxy.capacity -= 1
        chosen_proxy.save()
        return chosen_proxy

    # ################ Enem19 implementation ################

    active_proxies = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all()
    client_assignments = Assignment.objects.filter(client=client)
    known_blocked_proxies_for_client = client_assignments.values('proxy').filter(is_blocked=True)
    
    blocked_proxy_usage = 0
    for proxy in known_blocked_proxies_for_client:
        if not ProxyReport.objects.filter(proxy=proxy).values('clients').contains(client):
            blocked_proxy_usage += 1

    number_of_blocked_proxies_that_a_user_knows = known_blocked_proxies_for_client.count()
    number_of_requests_for_new_proxies = client_assignments.count()
    proxy_utilization = ProxyReport.objects.filter(connected_clients__value=client).count()

    utility_values_for_client = []
    alpha1, alpha2, alpha3, alpha4, alpha5 = 1,1,1,1,1
    some_cap_value = 50
    for proxy in active_proxies:
        distance = get_normalized_distance((proxy.latitude, proxy.longitude), (client.latitude, client.longitude))
        proxy_utility = alpha1 * min(proxy_utilization, some_cap_value) \
                        - alpha2 * number_of_requests_for_new_proxies \
                        - alpha3 * blocked_proxy_usage \
                        - alpha4 * number_of_blocked_proxies_that_a_user_knows \
                        - alpha5 * distance
        utility_values_for_client.append(proxy_utility)
    
    utility_values_for_proxies = []
    beta1, beta2, beta3, beta4 = 1,1,1,1
    for proxy in active_proxies:
        distance = get_normalized_distance((proxy.latitude, proxy.longitude), (client.latitude, client.longitude))
        number_of_connected_clients = ProxyReport.objects.filter(proxy=proxy).last().connected_clients.count()
        number_of_clients_who_know_the_proxy = Assignment.objects.filter(proxy=proxy).values('client').distinct().count()
        total_utilization_of_proxy_for_users = 0
        client_utility =  beta1 * number_of_clients_who_know_the_proxy \
                        + beta2 * number_of_connected_clients \
                        + beta3 * total_utilization_of_proxy_for_users \
                        - beta4 * distance
        utility_values_for_proxies.append(client_utility)

    mults = []
    for i in range(len(utility_values_for_client)):
        mults.append(utility_values_for_client[i] * utility_values_for_proxies[i])

    chosen_proxy = active_proxies[mults.index(max(mults))]
    Assignment.objects.create(proxy=chosen_proxy, client=client)
    chosen_proxy.capacity -= 1
    chosen_proxy.save()
    return chosen_proxy
