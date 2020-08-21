from django.urls import path

from .views import register_page, login_page

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
]
