from django import forms
import re
from django.forms.extras.widgets import SelectDateWidget
from account.conf import settings
from account.hooks import hookset
from account.utils import get_user_lookup_kwargs
from django.utils.translation import ugettext_lazy as _
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


class AddThingForm(forms.Form):
    itemname = forms.CharField(
        label=_("Name of the Item"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    details = forms.CharField(
        label=_("Details"),
        max_length=100,
        widget=forms.TextInput(),
        required=True
    )

    rate = forms.IntegerField(
        label=_("Rate (Enter 0 for free)"),
        required = True
    )

    itemimage = forms.ImageField(
        label=_("Upload image of the item"),
        required = True
    )
    #validators may require here