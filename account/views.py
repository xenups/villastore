from django.shortcuts import render

from rest_framework.request import Request
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from account.models import ProfileImage, UserProfile
from account.serializers import ProfileImageSerializer, UserProfileSerializer


class ProfileImageViewSet(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    serializer_class = ProfileImageSerializer
    queryset = ProfileImage.objects.all()


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
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

