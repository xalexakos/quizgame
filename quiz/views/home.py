from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quiz.models import UserQuiz


@login_required(login_url='login_page')
def home_page(request):
    has_ongoing_quiz = False
    quiz_repr = ''

    user_quiz_history = []
    user_quiz = UserQuiz.objects.filter(user_id=request.user.id).prefetch_related('quiz').order_by('-completed_at')
    for q in user_quiz:
        if q.completed_at is None:
            has_ongoing_quiz = True
            quiz_repr = '%s' % q.quiz
        else:
            user_quiz_history.append({'quiz': '%s' % q, 'score': q.correct_answers, 'completed_at': q.completed_at})

    return render(request, 'quiz/home.html', {
        'has_ongoing_quiz': has_ongoing_quiz,
        'quiz_repr': quiz_repr,
        'user_quiz_history': user_quiz_history
    })
