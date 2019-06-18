import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.gis.geos import Point

from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from django.contrib.gis.db.models.functions import Distance

from store.models import UserProfile, Unit, UnitImage, ProfileImage
from store.serializers import UserProfileSerializer, UserSerializer, UnitSerializer, ProfileImageSerializer, \
    UnitImageSerializer


# Create your views here.

class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitsList(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    # filter_backends = (filters.SearchFilter,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # search_fields = ('number_of_balcony',)
    filter_fields = (
        'unit_heading', 'number_of_balcony', 'unit_floor_number', 'carpet_area', 'is_active',
        'unit_type','posted_by',)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
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


class ImagesUnitViewSet(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    serializer_class = UnitImageSerializer
    queryset = UnitImage.objects.all()


class ProfileImageViewSet(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    serializer_class = ProfileImageSerializer
    queryset = ProfileImage.objects.all()
