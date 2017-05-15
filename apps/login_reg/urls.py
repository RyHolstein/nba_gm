from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_page, name = "login_page"), # url for the login page
    url(r'^registration$', views.register_page, name = "register_page"), # url for registration page
    url(r'^registration/register$', views.register), #register POST
    url(r'^login$', views.login),
]
