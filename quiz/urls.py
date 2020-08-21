from django.urls import re_path

from .views import home_page, question_view_page

urlpatterns = [
    re_path(r'^$', home_page, name='home_page'),
    re_path(r'^quiz/(?P<quiz_id>\d+)/question/(?P<question_id>\d+)/$', question_view_page, name='question_view_page')
]
