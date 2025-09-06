from django.contrib import admin
from .models import UserImage, UserProfile

# Register your models here.

admin.site.register(UserImage)
admin.site.register(UserProfile)