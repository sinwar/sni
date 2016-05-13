from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from .views import SignupView, ProfileView, ProView


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/pro/(?P<pk>[a-zA-Z0-9_-]+)/$",ProView, name = "account_pro"),
    url(r"^account/profile/(?P<pk>\d+)/$",ProfileView.as_view(), name = "account_profile"),
    url(r"^account/signup/", SignupView.as_view(), name = "account_signup"),
    url(r"^account/", include("account.urls")),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
