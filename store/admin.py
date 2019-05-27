from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from store.models import UserProfile

admin.site.register(UserProfile)
