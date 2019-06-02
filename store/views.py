from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_simplejwt.state import User

from store.models import UserProfile, Unit
from store.serializers import UserProfileSerializer, UserSerializer, UnitSerializer, ProfileImageSerializer


# Create your views here.

class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitsList(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileViewSet(generics.ListCreateAPIView):

    def initialize_request(self, request, *args, **kwargs):
        if not isinstance(request, Request):
            request = super().initialize_request(request, *args, **kwargs)
        return request

    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
