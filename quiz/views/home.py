from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login_page')
def home_page(request):
    return render(request, 'quiz/home.html', {})
