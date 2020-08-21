from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from quiz.models import Answer, QuizQuestion


@login_required(login_url='login_page')
def question_view_page(request, quiz_id, question_id):
    try:
        quiz_question = QuizQuestion.objects.get(quiz_id=quiz_id, question_id=question_id)
    except QuizQuestion.DoesNotExist:
        return redirect('home_page')
    else:
        answers = Answer.objects.filter(question_id=quiz_question.question.pk).values('text')

        context = {
            'question_no': quiz_question.order,
            'question': quiz_question.question.text,
            'answers': answers
        }

    return render(request, 'quiz/quiz.html', context)
