from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.
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


class UnitType(models.Model):
    unit_type = models.CharField(max_length=20)

    def __str__(self):
        return self.unit_type


class Unit(models.Model):
    unit_heading = models.CharField(max_length=50, blank=True)
    unit_type = models.ForeignKey(UnitType, blank=True, null=True, on_delete=models.CASCADE, verbose_name="نوع خانه")
    number_of_bedroom = models.IntegerField(default=0, blank=True)
    number_of_bathroom = models.IntegerField(default=0, blank=True)
    number_of_balcony = models.IntegerField(default=0, blank=True)
    date_of_posting = jmodels.jDateField(blank=True, null=True, verbose_name="تاریخ انتشار")
    posted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True,
                                  null=True)
    is_active = models.BooleanField(default=True)
    unit_description = models.CharField(max_length=500, blank=True)
    carpet_area = models.IntegerField(default=0, blank=True)
    unit_floor_number = models.IntegerField(default=0, blank=True)
    is_airconitioned = models.BooleanField(default=False, blank=True)
    num_of_assigned_car_parking = models.IntegerField(default=0, blank=True)
    has_carpet = models.BooleanField(default=False, blank=True)
    is_centeral_fan_cooling = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.unit_heading


class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, related_name='images', on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to="media", blank=True)
