from django.urls import path

from .views import home_page, quiz_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('quiz/', quiz_page, name='quiz_page'),
]
