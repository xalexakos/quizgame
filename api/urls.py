from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('quiz/', views.QuizGameAPIView.as_view(), name='quiz')
]

urlpatterns = format_suffix_patterns(urlpatterns)
