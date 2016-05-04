import account.views

from .forms import SignupForm
from .models import UserProfile

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
