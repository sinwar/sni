from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms


class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField(label = 'Upload image', required = True)


class AddThing(forms.Form):
    itemname = forms.CharField(label="Name of the item", required= True)
    details = forms.CharField(label="Details", required=True)
    rate = forms.IntegerField(label="Rate(Enter 0 for free)", required=True)
    imageitem = forms.ImageField(label="upload image of the item", required=True)