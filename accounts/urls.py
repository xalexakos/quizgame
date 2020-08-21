from django.urls import path

from .views import registration_page, login_page

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', registration_page, name='registration_page'),
]
