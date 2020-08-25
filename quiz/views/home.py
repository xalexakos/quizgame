from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render

from quiz.models import Quiz
from utils import calculate_perc, get_quiz_executions, get_user_history


@login_required(login_url='login_page')
def home_page(request):
    has_ongoing_quiz = False
    quiz_repr = ''

    user_quiz_history = []
    user_quiz = get_user_history(user_id=request.user.id)

    for q in user_quiz:
        if q.completed_at is None:
            has_ongoing_quiz = True
            quiz_repr = '%s' % q.quiz
        else:
            while cache.get('qtr:%s:lock' % q.quiz_id) is not None:
                continue

            success_rate = calculate_perc(*get_quiz_executions(q.quiz_id))
            user_quiz_history.append({
                'quiz': '%s' % q, 'score': q.correct_answers,
                'success_rate': success_rate, 'completed_at': q.completed_at
            })

    return render(request, 'quiz/home.html', {
        'has_ongoing_quiz': has_ongoing_quiz,
        'quiz_repr': quiz_repr,
        'user_quiz_history': user_quiz_history,
        'remaining_quizzes': len(user_quiz_history) - Quiz.objects.count()
    })
