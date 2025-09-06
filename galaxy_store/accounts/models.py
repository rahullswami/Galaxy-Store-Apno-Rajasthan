from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userimage')
    image = models.ImageField(upload_to='profile_images/', default='default.jpg', blank=True, null=True)


    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, default='')
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
