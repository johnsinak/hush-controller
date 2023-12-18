from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import AnonymousUser

# Create your views here.

class AssignmentView(APIView):
    """
    Get a new proxy assigned
    """

    def get(self, request: Request):
        # if not request.user.is_staff:
        #     return Response(status=401, data="you don't have permission")
        
        return Response(data=f"you are2 {request.META['REMOTE_ADDR']} - {request.META['HTTP_USER_AGENT']} - {request.META['REMOTE_HOST']}", status=status.HTTP_200_OK)