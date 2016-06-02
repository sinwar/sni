from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static


from .views import SignupView, ProfileView, ProView, addThingCreate, homeView, buyitemview, removeitem, noticegenerate, notifications, deletenotification


urlpatterns = [
    url(r"^$", homeView, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^addthing/$",addThingCreate.as_view(), name="add_item"),
    url(r"^addthing/added/$",TemplateView.as_view(template_name = "sni/added.html"), name="added"),
    url(r"^buyitem/(?P<item_id>\d+)/$", buyitemview, name="buyitem"),
    url(r"^deleteitem/(?P<pk>\d+)/$", removeitem, name="removeitem"),
    url(r"^deletenotification/(?P<pk>\d+)/$", deletenotification, name="deletenotification"),
    url(r"^newnotice/(?P<type>[a-zA-Z]+)/(?P<pk>\d+)/(?P<pk1>\d+)/$",noticegenerate, name="noticegenerate"),
    url(r"^notifications/", notifications, name="notifications"),
    url(r"^account/pro/(?P<pk>[a-zA-Z0-9_-]+)/$",ProView, name = "account_pro"),
    url(r"^account/profile/(?P<pk>\d+)/$",ProfileView.as_view(), name = "account_profile"),
    url(r"^account/signup/", SignupView.as_view(), name = "account_signup"),
    url(r"^account/", include("account.urls")),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

