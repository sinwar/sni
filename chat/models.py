from __future__ import unicode_literals

from django.db import models

from django.conf import settings

import datetime

# Create your models here.

class chatmessage(models.Model):
    """
    model for all messages in chat
    """

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank =True, related_name = 'chatreceiver')
    sender = models.CharField(default=" ", max_length=30)
    text = models.TextField(default=" ")
    created = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return "{0}-{1}".format(self.receiver, self.sender)


