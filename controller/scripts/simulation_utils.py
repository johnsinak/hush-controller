from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from assignments.services.startup import id_to_nums
from random import randint
from time import time
from assignments.models import *
from scripts.config_basic import CENSORED_REGION_SIZE, MAX_PROXY_CAPACITY, CENSOR_UTILIZATION_RATIO, CLIENT_UTILITY_THRESHOLD
from scripts.deferred_acceptance import get_matched_clients


def calcualte_distance(point_1, point_2):
    return ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5

def get_normalized_distance(point_1, point_2):
    return calcualte_distance(point_1, point_2) / CENSORED_REGION_SIZE


def get_client_proxy_utilization(client, client_assignments, right_now):
    proxy_checker = {}
    clients_proxy_utilization = 0
    for assignment in client_assignments:
        if proxy_checker.get(assignment.proxy.id, None):
            continue
        if assignment.proxy.is_blocked == True:
            clients_proxy_utilization += assignment.proxy.blocked_at - assignment.assignment_time
        else:
            clients_proxy_utilization += right_now - assignment.assignment_time
        proxy_checker[assignment.proxy.id] = True
    if client.is_censor_agent:
        clients_proxy_utilization = clients_proxy_utilization * CENSOR_UTILIZATION_RATIO
    
    return clients_proxy_utilization


def request_new_proxy_new_client(client):
    chosen_proxy = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all().first()

    Assignment.objects.create(proxy=chosen_proxy, client=client)
    if Assignment.objects.filter(proxy=chosen_proxy, client=client).count() == 1:
        chosen_proxy.capacity -= 1
        chosen_proxy.save()
    return chosen_proxy

def request_new_proxy(proposing_clients, right_now:int):
    client_prefrences = {}
    proxy_prefrences = {}
    proxy_capacities = {}
    flagged_clients = []

    active_proxies = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all()

    for proxy in active_proxies:
        utility_values_for_clients = {}
        alpha1, alpha2, alpha3, alpha4, alpha5 = 1 ,50, 2, 10, 10
        some_cap_value = 50 * 24
        for client in proposing_clients:
            if client.flagged == True:
                continue
            # ################ Enem19 implementation ################
            client_assignments = Assignment.objects.filter(client=client).order_by('created_at')
            assigned_proxies_list = client_assignments.values_list('proxy', flat=True).distinct()
            known_blocked_proxies_for_client = Proxy.objects.filter(id__in=assigned_proxies_list, is_blocked=True)
            known_proxies_for_client = Proxy.objects.filter(id__in=assigned_proxies_list)
            
            blocked_proxy_usage = 0
            for assignment in client_assignments:
                if assignment.proxy.is_blocked == True:
                    blocked_proxy_usage += assignment.proxy.blocked_at - assignment.assignment_time

            number_of_blocked_proxies_that_a_user_knows = known_blocked_proxies_for_client.count()
            number_of_requests_for_new_proxies = client_assignments.count()
    
            clients_proxy_utilization = get_client_proxy_utilization(client, client_assignments, right_now)
            distance = get_normalized_distance((proxy.latitude, proxy.longitude), (client.latitude, client.longitude))
            client_utility = alpha1 * min(clients_proxy_utilization, some_cap_value) \
                            - alpha2 * number_of_requests_for_new_proxies \
                            - alpha3 * blocked_proxy_usage \
                            - alpha4 * number_of_blocked_proxies_that_a_user_knows \
                            - alpha5 * distance
            
            if client_utility < CLIENT_UTILITY_THRESHOLD:
                client.flagged = True
                client.save()
                flagged_clients.append(client)
            utility_values_for_clients[client.ip] = client_utility
        proxy_prefrences[proxy.ip] = list(reversed(sorted(utility_values_for_clients, key=lambda k: utility_values_for_clients[k])))
        proxy_capacities[proxy.ip] = proxy.capacity

    for client in proposing_clients:
        if client.flagged == True:
                continue
        # ################ Enem19 implementation ################
        utility_values_for_proxies = {}
        beta1, beta2, beta3, beta4 = 1,1,1,1
        for proxy in active_proxies:
            distance = get_normalized_distance((proxy.latitude, proxy.longitude), (client.latitude, client.longitude))
            number_of_connected_clients = MAX_PROXY_CAPACITY - proxy.capacity
            number_of_clients_who_know_the_proxy = Assignment.objects.filter(proxy=proxy).values_list('client', flat=True).distinct().count()
            total_utilization_of_proxy_for_users = 0
            proxy_utility =  beta1 * number_of_clients_who_know_the_proxy \
                            + beta2 * number_of_connected_clients \
                            + beta3 * total_utilization_of_proxy_for_users \
                            - beta4 * distance
            utility_values_for_proxies[proxy.ip] = proxy_utility
        client_prefrences[client.ip] = list(reversed(sorted(utility_values_for_proxies, key=lambda k: utility_values_for_proxies[k])))
        
    matches = get_matched_clients(client_prefrences, proxy_prefrences, proxy_capacities)

    for proxy_id in matches.keys():
        proxy = Proxy.objects.get(ip=proxy_id)
        clients_accepted = matches[proxy_id]
        for client_ip in clients_accepted:
            client = Client.objects.get(ip=client_ip)
            Assignment.objects.create(proxy=proxy, client=client, assignment_time=right_now)
            if Assignment.objects.filter(proxy=proxy, client=client).count() == 1:
                    proxy.capacity -= 1
                    proxy.save()

    return matches, flagged_clients
