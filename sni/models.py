from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    first_name = models.TextField(default=" ")
    last_name = models.TextField(default=" ")

    def __str__(self):
    	return "{0}-{1}".format(self.first_name, self.last_name)