from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
import django.contrib.auth.password_validation as validators
from drf_extra_fields.geo_fields import PointField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from account.serializers import UserProfileSerializer, UserSerializer
from store.models import UserProfile, Unit, UnitImage, UnitType, Location


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'


class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ('image', 'unit',)

        def validate(self, data):
            # get the password from the data
            password = data.get('password')

            errors = dict()
            try:
                # validate the password and catch the exception
                validators.validate_password(password=password, user=User)

            # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

            if errors:
                raise serializers.ValidationError(errors)

            return super(UserSerializer, self).validate(data)

        def create(self, validated_data):
            unit_data = validated_data.pop('unit')
            unit = UnitSerializer.create(UnitSerializer(), validated_data=unit_data)
            images_data = self.context.get('view').request.FILESz
            for image_data in images_data.values():
                UnitImage.objects.create(image=image_data, pk=unit_data.pk)
            return UnitImage


class LocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'address', 'city', 'state',)
        geo_field = 'point'


class UnitSerializer(serializers.ModelSerializer, ):
    images = UnitImageSerializer(many=True, read_only=True)
    location = LocationSerializer()
    unit_type = UnitTypeSerializer()
    posted_by = UserProfileSerializer()

    def to_internal_value(self, data):
        # when object received here changed to the object view
        # it changed the nested object to flat
        # just work while using post
        self.fields['posted_by'] = serializers.PrimaryKeyRelatedField(
            queryset=UserProfile.objects.all())

        self.fields['unit_type'] = serializers.PrimaryKeyRelatedField(
            queryset=UnitType.objects.all())

        return super(UnitSerializer, self).to_internal_value(data)

    class Meta:
        model = Unit
        # fields = '__all__'
        fields = ('id', 'location', 'unit_heading', 'unit_type', 'posted_by', 'carpet_area',
                  'date_of_posting', 'has_carpet', 'is_active', 'is_airconitioned', 'is_centeral_fan_cooling',
                  'num_of_assigned_car_parking', 'number_of_balcony', 'number_of_bathroom', 'number_of_bedroom',
                  'unit_description', 'unit_floor_number', 'images',)

    def create(self, validated_data):
        print("create called")
        postedby_data = validated_data.pop('posted_by')
        unitType_data = validated_data.pop('unit_type')
        location_data = validated_data.pop('location')

        unit = Unit.objects.create(**validated_data)
        postedby, created = UserProfile.objects.get_or_create(pk=postedby_data.pk)
        unitType, created = UnitType.objects.get_or_create(pk=unitType_data.pk)

        location = LocationSerializer.create(LocationSerializer(), validated_data=location_data)
        # locationD,created = Location.objects.get_or_create(location_data)
        # locationD.city = 'hiii'

        # unit.location = locationD
        unit.posted_by = postedby
        unit.location = location
        unit.unit_type = unitType
        unit.save()
        unit.unit_heading = validated_data['unit_heading']
        unit.carpet_area = validated_data['carpet_area']
        unit.date_of_posting = validated_data['date_of_posting']
        unit.has_carpet = validated_data['has_carpet']
        unit.is_active = validated_data['is_active']
        unit.is_airconitioned = validated_data['is_airconitioned']
        unit.is_centeral_fan_cooling = validated_data['is_centeral_fan_cooling']
        unit.num_of_assigned_car_parking = validated_data['num_of_assigned_car_parking']
        unit.number_of_balcony = validated_data['number_of_balcony']
        unit.number_of_bathroom = validated_data['number_of_bathroom']
        unit.number_of_bedroom = validated_data['number_of_bedroom']
        unit.unit_description = validated_data['unit_description']
        unit.unit_floor_number = validated_data['unit_floor_number']
        unit.save()
        return unit

    def update(self, instance, validated_data):
        print("update call")
        postedby_data = validated_data.pop('posted_by')
        unitType_data = validated_data.pop('unit_type')

        postedby, created = UserProfile.objects.get_or_create(pk=postedby_data.pk)
        unitType, created = UnitType.objects.get_or_create(pk=unitType_data.pk)

        instance.posted_by = postedby
        instance.unit_type = unitType
        instance.save()
        instance.unit_heading = validated_data['unit_heading']
        instance.carpet_area = validated_data['carpet_area']
        instance.date_of_posting = validated_data['date_of_posting']
        instance.has_carpet = validated_data['has_carpet']
        instance.is_active = validated_data['is_active']
        instance.is_airconitioned = validated_data['is_airconitioned']
        instance.is_centeral_fan_cooling = validated_data['is_centeral_fan_cooling']
        instance.num_of_assigned_car_parking = validated_data['num_of_assigned_car_parking']
        instance.number_of_balcony = validated_data['number_of_balcony']
        instance.number_of_bathroom = validated_data['number_of_bathroom']
        instance.number_of_bedroom = validated_data['number_of_bedroom']
        instance.unit_description = validated_data['unit_description']
        instance.unit_floor_number = validated_data['unit_floor_number']
        instance.save()

        return instance
