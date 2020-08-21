from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login_page')
def quiz_page(request):
    context = {
        'question': 'Which is the best programming language?',
        'answers': [
            {'no': 0, 'text': 'Java'},
            {'no': 1, 'text': 'Python'},
            {'no': 2, 'text': 'Ruby'},
            {'no': 3, 'text': 'Kotlin'},
        ]
        }
    return render(request, 'quiz/quiz.html', context)
