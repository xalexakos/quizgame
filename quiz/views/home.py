from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quiz.models import UserQuiz


@login_required(login_url='login_page')
def home_page(request):
    has_ongoing_quiz = False
    quiz_repr = ''

    ongoing_quiz = UserQuiz.objects.filter(user_id=request.user.id, completed_at__isnull=True).first()
    if ongoing_quiz:
        has_ongoing_quiz = True
        quiz_repr = '%s' % ongoing_quiz.quiz

    return render(request, 'quiz/home.html', {
        'has_ongoing_quiz': has_ongoing_quiz,
        'quiz_repr': quiz_repr
    })
