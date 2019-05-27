from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django_jalali.admin import JDateFieldListFilter

from store.models import UserProfile, Unit, UnitType, UserType, UnitImage


class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 3


class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitImageInline, ]
    list_filter = (
        ('date_of_posting', JDateFieldListFilter),)


admin.site.register(UserProfile)
admin.site.register(UserType)
admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitType)
