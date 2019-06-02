from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
import django.contrib.auth.password_validation as validators

from store.models import UserProfile, Unit, UnitImage, UnitType, ProfileImage, UserType


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        # user = User(**data)

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
        user = User.objects.create(**validated_data)
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.save()
        return user

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        instance.password = user.get('password')
        instance.email = user.get('email')
        instance.first_name = user.get('first_name')
        instance.last_name = user.get('last_name')
        instance.save()
        return instance


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('image', 'userprofile')

        def create(self, validated_data):
            userprofile_data = validated_data.pop('userprofile')
            userimage = ProfileImageSerializer.create(ProfileImageSerializer(), validated_data=userprofile_data)
            images_data = self.context.get('view').request.FILES
            for image_data in images_data.values():
                ProfileImage.objects.create(image=image_data, pk=userprofile_data.pk)
            return ProfileImage


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('user_type',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    user_type = UserTypeSerializer()
    images = ProfileImageSerializer(source='profileimage_set', many=True, read_only=True)

    def to_internal_value(self, data):
        # when object received here changed to the object view
        # it changed the nested object to flat
        # just work while using post
        self.fields['user_type'] = serializers.PrimaryKeyRelatedField(
            queryset=UserType.objects.all())
        return super(UserProfileSerializer, self).to_internal_value(data)

    class Meta:
        model = UserProfile
        fields = ('bio', 'user', 'images', 'user_type')

    def create(self, validated_data):
        userType_data = validated_data.pop('user_type')
        userType, created = UserType.objects.get_or_create(pk=userType_data.pk)

        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        userprofile = UserProfile.objects.create(user=user, bio=validated_data.pop('bio'), user_type=userType)
        images_data = self.context.get('view').request.FILES

        userprofile.save()
        return userprofile


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'


class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ('image', 'unit',)

        def create(self, validated_data):
            unit_data = validated_data.pop('unit')
            unit = UnitSerializer.create(UnitSerializer(), validated_data=unit_data)
            images_data = self.context.get('view').request.FILES
            for image_data in images_data.values():
                UnitImage.objects.create(image=image_data, pk=unit_data.pk)
            return UnitImage


class UnitSerializer(serializers.ModelSerializer):
    images = UnitImageSerializer(many=True, read_only=True)
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
        fields = ('id', 'unit_heading', 'unit_type', 'posted_by', 'carpet_area',
                  'date_of_posting', 'has_carpet', 'is_active', 'is_airconitioned', 'is_centeral_fan_cooling',
                  'num_of_assigned_car_parking', 'number_of_balcony', 'number_of_bathroom', 'number_of_bedroom',
                  'unit_description', 'unit_floor_number', 'images')

    def create(self, validated_data):
        postedby_data = validated_data.pop('posted_by')
        unitType_data = validated_data.pop('unit_type')

        unit = Unit.objects.create(**validated_data)
        postedby, created = UserProfile.objects.get_or_create(pk=postedby_data.pk)
        unitType, created = UnitType.objects.get_or_create(pk=unitType_data.pk)

        unit.posted_by = postedby
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
