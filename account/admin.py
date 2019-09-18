from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django_jalali.admin import JDateFieldListFilter

from account.models import ProfileImage, UserProfile, UserType


class UserProfileImageline(admin.TabularInline):
    model = ProfileImage
    extra = 3


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileImageline, ]
    # filter_horizontal = (UserProfileImageline,)


admin.site.register(UserType)
admin.site.register(UserProfile, UserProfileAdmin)
