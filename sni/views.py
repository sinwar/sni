
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
from .models import UserProfile, addThing, newnotice
from account.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# signup view overwrided
class SignupView(account.views.SignupView):

    form_class = SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user = self.created_user,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            image = form.cleaned_data["image"],
            mobile = form.cleaned_data["mobile"],
            facebook = form.cleaned_data["facebook"],
            address = form.cleaned_data["address"]
            )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

@login_required
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
    things = addThing.objects.filter(owner = pk)
    cout = len(things)
    return render(request, 'sni/profile.html', {'user':user, 'var':var, 'things':things, 'cout':cout})

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


# view for item details or buyitem
@login_required
def buyitemview(request, item_id):
    thing = addThing.objects.get(pk = item_id)
    profile = UserProfile.objects.get(user = thing.owner)
    path = ""
    for i in reversed(thing.itemimage.url):
        if i == '/':
            break
        else:
            path = i + path
    path = "{0}{1}{2}".format(settings.MEDIA_URL, "/things/", path)
    return render(request, 'sni/buyitem.html',{'thing':thing, 'profile':profile, 'path':path})

# view for remove item
@login_required
def removeitem(request, pk):
    item = get_object_or_404(addThing, pk = pk)
    item.delete()
    return redirect('sni.views.homeView')


# function for generate new notice to owner
'''
def noticegen(type, sender, receiver, message):
    notice = newnotice.objects.create(sender=sender, type=type, receiver=receiver, message=message) return notice '''



# view for generate new notice to owner
@login_required
def noticegenerate(request, type, pk, pk1):
    # receiver is the owner of the thing so pk relate to reciever
    receiverobject = get_object_or_404(UserProfile, pk = pk)
    receiver = receiverobject.user
    # pk1 relate to the item
    item = get_object_or_404(addThing, pk = pk1)
    if type == 'request':
        message = "{0} wants to buy {1} added by you".format(request.user, item)
    else:
        message = "Your request for {0} is accepted by {1}".format(item, request.user)
    newnotice.objects.create(sender=request.user,receiver=receiver, message=message, type=type)
    return redirect('sni.views.buyitemview', item_id = pk1)

# view for all the notification of user
@login_required
def notifications(request):
    notification = newnotice.objects.filter(receiver=request.user)
    itemlist =[]
    typ = []
    if len(notification) != 0:
        for i in notification:
            k = i.message.split(" ")
            if i.type == 'request':
                item = k[4]
                try:
                    itemlist.append(addThing.objects.get(itemname=item))
                except ObjectDoesNotExist:
                    pass
            typ.append(i.type)
    if len(itemlist) != 0:
        notification = zip(notification, itemlist, typ)
    else:
        notification = zip(notification, typ)

    lengthnotifications = len(notification)

    return render(request, 'sni/notifications.html',{'notification':notification, 'lenghtnotifications':lengthnotifications})

@login_required
def deletenotification(request, pk):
    notification = get_object_or_404(newnotice, pk=pk)
    item = notification.message.split(" ")
    message = "Your request for {0} is declined by {1}".format(item[4], notification.receiver)
    if notification.type == 'request':
        newnotice.objects.create(sender=request.user, type='decline', receiver=notification.sender, message=message)
    notification.delete()
    return redirect('sni.views.notifications')


@login_required
def removeitemonaccept(request, pk, pk1):
    item = get_object_or_404(addThing, pk = pk)
    notification = get_object_or_404(newnotice, pk=pk1)
    message = "Your request for {0} is accepted by {1}".format(item, notification.receiver)
    newnotice.objects.create(sender=request.user, type='accept', receiver=notification.sender, message=message)
    notification.delete()
    item.delete()
    return redirect('sni.views.notifications')

