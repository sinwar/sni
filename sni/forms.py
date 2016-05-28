from django import forms
import re
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from account.conf import settings
from account.hooks import hookset
from account.utils import get_user_lookup_kwargs
from django.utils.translation import ugettext_lazy as _
from . import models
import account.forms


class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField(
        label = _("First Name"),
        max_length = 30,
        required = True
    )
    last_name = forms.CharField(
        label =_("Last Name"),
        max_length = 30,
        required = True
    )
    image = forms.ImageField(
        label = _("Upload image"),
        required = True
    )

    mobile = forms.IntegerField(
        label = _("mobile number"),
        required = True
    )

    facebook = forms.URLField(
        label = _("facebook profile"),
        required = True
    )


class addThingForm(ModelForm):

    class Meta:
        model = models.addThing
        fields = ['itemname', 'details', 'rate', 'itemimage']
    #validators may require here