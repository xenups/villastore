from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django_jalali.admin import JDateFieldListFilter

from store.models import UserProfile, Unit, UnitType, UserType, UnitImage, ProfileImage


class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 3


class UserProfileImageline(admin.TabularInline):
    model = ProfileImage
    extra = 3


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileImageline, ]
    # filter_horizontal = (UserProfileImageline,)


class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitImageInline, ]
    list_filter = (
        ('date_of_posting', JDateFieldListFilter),)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserType)
admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitType)
