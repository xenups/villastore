import django_filters
from rest_framework.permissions import AllowAny

from rest_framework_gis.filters import DistanceToPointFilter, InBBoxFilter
from rest_framework import generics, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .permissions import *
from store.models import Unit, UnitImage, Location
from store.serializers import UnitSerializer, UnitImageSerializer, LocationSerializer


class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
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


class ImagesUnitViewSet(generics.ListCreateAPIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    serializer_class = UnitImageSerializer
    queryset = UnitImage.objects.all()
