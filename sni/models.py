from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    first_name = models.TextField(default=" ")
    last_name = models.TextField(default=" ")
    image = models.ImageField(default=" ", upload_to = settings.MEDIA_URL)
    def __str__(self):
    	return "{0}".format(self.user)