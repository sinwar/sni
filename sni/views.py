from django.http import Http404, HttpResponseForbidden, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.views.generic import TemplateView, DetailView
import account.views
from .forms import SignupForm
from .models import UserProfile
from account.conf import settings

class SignupView(account.views.SignupView):

    form_class = SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user = self.created_user,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

class ProView(TemplateView):
    template_name = "sni/profile.html"
    model = UserProfile
    
    def get_context_data(self, request, **kwargs):
        context = super(ProView, self).get_context_data(**kwargs)
        context["first_name"] = UserProfile.objects.get(pk=request.user.id)
        context["last_name"] = 'last_name'
        return context

class ProfileView(DetailView):
    model = UserProfile