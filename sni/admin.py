from django.contrib import admin
from .models import UserProfile, addThing, newnotice

admin.site.register(UserProfile)
admin.site.register(addThing)
admin.site.register(newnotice)