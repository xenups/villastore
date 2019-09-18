from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models

from rest_framework.exceptions import ValidationError


class UserType(models.Model):
    user_type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user_type


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=False)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class ProfileImage(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.FileField(blank=True)

    def __str__(self):
        return self.userprofile.bio
