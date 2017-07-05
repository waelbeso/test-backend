from django.conf.urls import include, url
from accounts import views

urlpatterns = [
    url(r'^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', views.UserView ),
    url(r'^$', views.Registration ),
    url(r'^addresses/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', views.UserAddressView ),
    url(r'^addresses', views.UserAddressView ),
    ]