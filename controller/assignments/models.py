import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    PermissionsMixin,
)
import requests


def get_ip_location(ip: str):
    base_url = f"http://ipapi.co/{ip}/json/"
    response = requests.get(base_url)
    location = response.json()
    return location["latitude"], location["longitude"]


class ProxyManager(models.Manager):
    def create(self, **kwargs):
        proxy_ip = kwargs.get('ip', None)
        is_test = kwargs.get('is_test', None)
        if proxy_ip is not None and is_test is not True:
            latitude, longitude = get_ip_location(proxy_ip)
            kwargs['latitude'] = latitude
            kwargs['longitude'] = longitude
        else:
            kwargs['latitude'] = 0.0
            kwargs['longitude'] = 0.0
        instance = super().create(**kwargs)

        return instance


class Proxy(models.Model):
    url = models.CharField(max_length=100, null=True)
    ip = models.CharField(max_length=30, null=False, default='0.0.0.0')
    is_test = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    capacity = models.IntegerField(default=40)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    objects = ProxyManager()

    def __str__(self):
        return str(self.url)


class ClientManager(models.Manager):
    def create(self, **kwargs):
        user_ip = kwargs.get('ip', None)
        is_test = kwargs.get('is_test', None)
        if user_ip is not None and is_test is not True:
            latitude, longitude = get_ip_location(user_ip)
            kwargs['latitude'] = latitude
            kwargs['longitude'] = longitude
        else:
            kwargs['latitude'] = 0.0
            kwargs['longitude'] = 0.0
        instance = super().create(**kwargs)

        return instance


class Client(models.Model):
    ip = models.CharField(max_length=30, null=False, unique=True, primary_key=True)
    is_test = models.BooleanField(default=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    objects = ClientManager()


class ProxyReport(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    proxy = models.ForeignKey(
        Proxy,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reports_given",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    utility = models.FloatField()
    throughput = models.FloatField()
    connected_clients = models.ManyToManyField(
        Client, related_name="proxies_connected", blank=True
    )


class Assignment(models.Model):
    proxy = models.ForeignKey(
        Proxy,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="assignee",
    )
    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="assigned",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class IDClientCounter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class ClientAvgMigrationTime(models.Model):
    value = models.FloatField()
    client_ip = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)


class ProxyAvgMigrationTime(models.Model):
    value = models.FloatField()
    proxy_ip = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)