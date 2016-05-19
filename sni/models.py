from django.conf import settings
from django.db import models
import datetime

class addThing(models.Model):
    itemname = models.CharField(default=" ", max_length=30)
    details = models.TextField(default=" ")
    rate = models.IntegerField(default=" ")
    itemimage = models.ImageField(default=" ", upload_to = settings.MEDIA_ROOT+"/things/")
    datetime = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return "{0}".format(self.itemname)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    first_name = models.TextField(default=" ")
    last_name = models.TextField(default=" ")
    image = models.ImageField(default=" ", upload_to = settings.MEDIA_ROOT)
    items = models.ForeignKey(addThing, on_delete = models.CASCADE, null = True, blank =True)
    def __str__(self):
    	return "{0}".format(self.user)

