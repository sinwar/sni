from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms


class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField(label = 'Upload image', required = True)