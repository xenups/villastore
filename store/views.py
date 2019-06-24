import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.gis.geos import Point

from rest_framework_gis.filters import DistanceToPointFilter, InBBoxFilter
from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from django.contrib.gis.db.models.functions import Distance
from .permissions import *
from store.models import UserProfile, Unit, UnitImage, ProfileImage, Location
from store.serializers import UserProfileSerializer, UserSerializer, UnitSerializer, ProfileImageSerializer, \
    UnitImageSerializer, LocationSerializer


# Create your views here.

class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class LocationList(generics.ListCreateAPIView):
    # this is an instance of distance to location
    # http://127.0.0.1:8000/api/location/?dist=4000&point=-122.4862,37.7694
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True
    filter_fields = ('city', 'address',)


class UnitsList(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    # filter_backends = (filters.SearchFilter,)
    # http://127.0.0.1:8000/api/units/?in_bbox=48.47,36.92,49.95,37.56 find locations that exist in rasht
    bbox_filter_field = 'location__point'
    bbox_filter_include_overlapping = True
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, InBBoxFilter,)
    # search_fields = ('number_of_balcony',)
    filter_fields = (
        'unit_heading', 'number_of_balcony', 'unit_floor_number', 'carpet_area', 'is_active',
        'unit_type', 'posted_by', 'location__city', 'location__address',)


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
