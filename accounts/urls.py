from django.urls import re_path

from .views import registration_page, login_page

urlpatterns = [
    re_path(r'^login/$', login_page, name='login_page'),
    re_path(r'^register/$', registration_page, name='registration_page'),
]
