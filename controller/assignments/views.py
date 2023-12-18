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

from assignments.models import Client


# Create your views here.

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

        # TODO: create an assignment