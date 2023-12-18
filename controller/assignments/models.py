import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    PermissionsMixin,
)


class Proxy(models.Model):
    url = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    # summon_date = models.DateTimeField(auto_now=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # verified_attenders = models.ManyToManyField(
    #     User, related_name="events_attending", blank=True
    # )
    is_blocked = models.BooleanField(default=True)

    def __str__(self):
        return str(self.url)


class Client(models.Model):
    ip = models.CharField(max_length=30, null=False)
    user_agent = models.CharField(max_length=255, null=True, blank=True)


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
    # TODO: ask about this
    connected_users = models.ManyToManyField(
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

