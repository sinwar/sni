from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.TextField(default=" ")
    last_name = models.TextField(default=" ")