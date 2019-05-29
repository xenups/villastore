from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from store.models import UserProfile, Unit
from store.serializers import UserProfileSerializer, UserSerializer, UnitSerializer


# Create your views here.

class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitsList(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
