from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from assignments.services.startup import id_to_nums
from scripts.config_basic import CENSORED_REGION_SIZE
from random import randint
from time import time
import socket

from assignments.models import *


def calcualte_distance(point_1, point_2):
    return ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5


def get_normalized_distance(point_1, point_2):
    return calcualte_distance(point_1, point_2) / CENSORED_REGION_SIZE

class AssignmentView(APIView):
    """
    Get a new proxy assigned
    """

    def get(self, request: Request):
        user_ip = request.META.get('REMOTE_ADDR', None)
        if not user_ip:
            return Response(data=f"No Ip reported.", status=status.HTTP_400_BAD_REQUEST)

        user_device = request.META.get('HTTP_USER_AGENT', 'N/A')
        try:
            client = Client.objects.get(ip=user_ip)
        except ObjectDoesNotExist:
            client = Client.objects.create(ip=user_ip, user_agent=user_device)
            # provide with random proxy and done. discuss this
            active_proxies = Proxy.objects.filter(is_blocked=False, is_active=True, capacity__gt=0).all()
            chosen_proxy = active_proxies[randint(0,len(active_proxies) - 1)]
            Assignment.objects.create(proxy=chosen_proxy, client=client)
            chosen_proxy.capacity -= 1
            chosen_proxy.save()
            return Response(data=f"{chosen_proxy.ip}", status=status.HTTP_200_OK)

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
        return Response(data=f"{chosen_proxy.ip}", status=status.HTTP_200_OK)

class ProxyUpdateView(APIView):
    """
    submit a change to the proxy infrastructure
    """

    def post(self, request: Request):
        # TODO: Migrating everything for now, fix later maybe!
        start_time = time()
        source_id = request.data['source_id']
        proxy_len = request.data['proxy_len']
        base_proxy_ip = '1.{}.{}.{}'

        for proxy_id in range(proxy_len):
            num1, num2 = id_to_nums(proxy_id)
            proxy_ip = base_proxy_ip.format(num1, num2, source_id)
            proxy = Proxy.objects.get(ip=proxy_ip)
            clients = Assignment.objects.filter(proxy=proxy).values_list('client', flat=True)
            new_proxy_ip = base_proxy_ip.format(num1, num2, source_id + 1)
            new_proxy = Proxy.objects.get(ip=new_proxy_ip)
            for client_ip in clients:
                client = Client.objects.get(ip=client_ip)
                Assignment.objects.create(client=client, proxy=new_proxy)
            migration_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            migration_socket.connect(("54.145.21.93", 8000))
            migration_socket.send(f"migrate {new_proxy_ip}".encode())
            migration_socket.close()

        duration = time() - start_time
        ControllerAvgMigrationTime.objects.create(value=duration)

        return Response(data=f"Updated assignments and sent migration info! duration: {duration}", status=status.HTTP_200_OK)
        


class IDAssignmentView(APIView):
    """
    submit a change to the proxy infrastructure
    """

    def get(self, request: Request):
        new_id = IDClientCounter.objects.count() + 3
        IDClientCounter.objects.create()


        return Response(data=f"{new_id}", status=status.HTTP_200_OK)

    def post(self, request: Request):
        IDClientCounter.objects.all().delete()

        return Response(data=f"everything nuked!", status=status.HTTP_200_OK)


class ClientAvgPostView(APIView):
    """
    submit average time of migration for proxy
    """

    def post(self, request: Request):
        try:
            avg_time = float(request.data['avg'])
            user_ip = request.META.get('REMOTE_ADDR', None)
        except:
            return Response(data=f"bad request", status=status.HTTP_400_BAD_REQUEST)
        
        obj = ClientAvgMigrationTime.objects.create(client_ip=user_ip, value=avg_time)

        return Response(data=f"created, val: {obj.value}!", status=status.HTTP_200_OK)


class ProxyAvgPostView(APIView):
    """
    submit average time of migration for proxy
    """

    def post(self, request: Request):
        try:
            avg_time = float(request.data['avg'])
            proxy_ip = request.META.get('REMOTE_ADDR', None)
        except:
            return Response(data=f"bad request", status=status.HTTP_400_BAD_REQUEST)
        
        obj = ProxyAvgMigrationTime.objects.create(proxy_ip=proxy_ip, value=avg_time)

        return Response(data=f"created, val: {obj.value}!", status=status.HTTP_200_OK)