from django.http import Http404, HttpResponseForbidden, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, render
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
            image = form.cleaned_data["image"],
            )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

def ProView(request, pk):
    user = get_object_or_404(UserProfile, user__pk=pk)
    return render(request, 'sni/profile.html', {'user':user})

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