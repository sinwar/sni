from django.conf import settings
from django.db import models
from django import utils
import datetime


class UserProfile(models.Model):
    """
    model for storing user information for authenticated user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    first_name = models.TextField(default = " ")
    last_name = models.TextField(default = " ")
    image = models.ImageField(default = " ", upload_to = settings.MEDIA_ROOT)
    mobile = models.TextField(default = " ")
    address = models.TextField(default = " ")
    facebook = models.TextField(default = " ")
    def __str__(self):
    	return "{0}".format(self.user)


class addThing(models.Model):
    """
    model for storing items added by user
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank =True, related_name = 'owneruser')
    itemname = models.CharField(default=" ", max_length=30)
    details = models.TextField(default=" ")
    rate = models.IntegerField(default=" ")
    itemimage = models.ImageField(default=" ", upload_to = settings.MEDIA_ROOT+"/things/")
    datetime = models.DateTimeField(default=utils.timezone.now)
    def __str__(self):
        return "{0}".format(self.itemname)

    def get_absolute_url(self):
        return "/buyitem/%i/" % self.id



class newnotice(models.Model):
    """
    model for send notification for buy the thing
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank =True, related_name = 'noticesender')
    receiver = models.CharField(default=" ", max_length = 30)
    message = models.TextField(default=" ")
    type = models.CharField(default=" ", max_length=30)

    def __str__(self):
        return "{0}-{1}".format(self.sender, self.message)