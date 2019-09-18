from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
import django.contrib.auth.password_validation as validators

from account.models import ProfileImage
from account.models import UserProfile, UserType


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

        userprofile.save()
        return userprofile

    def update(self, instance, validated_data):
        print("update call")
        user = validated_data.get('user')
        instance.user.first_name = user.get('first_name')
        instance.user.last_name = user.get('last_name')
        instance.user.set_password(user.get('password'))
        instance.user.email = user.get('email')
        # every instances entity must be saved before return
        instance.user.save()

        instance.bio = validated_data['bio']
        instance.save()
        return instance
