
from __future__ import unicode_literals

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView

from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from account import signals
from account.conf import settings
from account.forms import SignupForm, LoginUsernameForm
from account.forms import ChangePasswordForm, PasswordResetForm, PasswordResetTokenForm
from account.forms import SettingsForm
from account.hooks import hookset
from account.mixins import LoginRequiredMixin
from account.models import SignupCode, EmailAddress, EmailConfirmation, Account, AccountDeletion
from account.utils import default_redirect, get_form_data

from django.http import Http404, HttpResponseForbidden, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, CreateView
import account.views
from .forms import SignupForm, addThingForm
from .models import UserProfile, addThing
from account.conf import settings

# signup view overwrided
class SignupView(account.views.SignupView):

    form_class = SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user = self.created_user,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            image = form.cleaned_data["image"],
            )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

# profile view
def ProView(request, pk):
    user = get_object_or_404(UserProfile, user__pk=pk)
    path = ""
    for i in reversed(user.image.url):
        if i == '/':
            break
        else:
            path = i+path
    var = "{0}{1}".format(settings.MEDIA_URL, path)
    return render(request, 'sni/profile.html', {'user':user, 'var':var})

'''
class ProView(TemplateView):
    template_name = "sni/profile.html"
    model = UserProfile
    
    def get_context_data(self, **kwargs):
        context = super(ProView, self).get_context_data(**kwargs)
        context["first_name"] = get_object_or_404(UserProfile, pk=user)
        context["last_name"] = 'last_name'
        return context
'''
# profile detail view
class ProfileView(DetailView):
    model = UserProfile

# createview for add item
class addThingCreate(CreateView):
    template_name = "sni/addThing_create_form.html"
    form_class = addThingForm
    success_url = '/addthing/added/'
    model = addThing
    # adding current user using validation
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(addThingCreate, self).form_valid(form)


# view for show allthing on homepage in chronological order
def homeView(request):
    things = addThing.objects.all().order_by("-datetime")
    list=[]
    for i in things:
        path=""
        for j in reversed(i.itemimage.url):
            if j == '/':
                break
            else:
                path = j+path
        list.append("{0}{1}{2}".format(settings.MEDIA_URL, "/things/", path))
    things=zip(things, list)
    return render(request, 'homepage.html',{'things':things})