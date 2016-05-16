from django.http import Http404, HttpResponseForbidden, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
import account.views
from .forms import SignupForm, AddThingForm
from .models import UserProfile
from account.conf import settings

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

def ProView(request, pk):
    user = get_object_or_404(UserProfile, user__pk=pk)
    path = ""
    for i in reversed(user.image.url):
        if i == '/':
            break
        else:
            path = i+path;
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
class ProfileView(DetailView):
    model = UserProfile

class itemview(FormView):
    template_name = "sni/item.html"
    form_class = AddThingForm
    identifier_field = "itemname"
    form_kwargs = {}
    success_url = '/added/'#bug

    def form_valid(self, form):
       return super(itemview, self).form_valid(form)
    