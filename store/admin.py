from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from store.models import UserProfile, Unit, UnitType, UserType

admin.site.register(UserProfile)
admin.site.register(UserType)
admin.site.register(Unit)
admin.site.register(UnitType)
