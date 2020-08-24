from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('quiz/', views.QuizGameAPIView.as_view(), name='quiz'),
    path('quiz/success-rate/', views.QuizGameSuccessRateAPIView.as_view(), name='quiz_success_rate')
]

urlpatterns = format_suffix_patterns(urlpatterns)
