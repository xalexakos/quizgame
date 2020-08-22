from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from quiz.models import Answer, QuizQuestion, UserQuiz, Quiz, UserQuizAnswer


@login_required(login_url='login_page')
def question_view_page(request, quiz_id, question_id):
    """ Renders a question with its related answers. """
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


@login_required(login_url='login_page')
def start_quiz(request):
    """ Starts a new quest or populate the next question of an ongoing one. """
    try:
        user_quiz = UserQuiz.objects.get(completed_at__isnull=True, user_id=request.user.id)
    except UserQuiz.DoesNotExist:
        quiz = Quiz.objects.random()
        UserQuiz.objects.create(user_id=request.user.id, quiz_id=quiz.id)
        quiz_question = QuizQuestion.objects.get(quiz_id=quiz.id, order=1)

        quiz_id = quiz.id
        question_id = quiz_question.question_id
    else:
        # find the next question to be answered.
        submitted_questions = UserQuizAnswer.objects.filter(userquiz_id=user_quiz.id).values_list('question_id')
        quiz_question = QuizQuestion.objects.filter(quiz_id=user_quiz.quiz_id) \
            .exclude(question_id__in=submitted_questions) \
            .order_by('order')

        if quiz_question.exists():
            quiz_id = quiz_question[0].quiz_id
            question_id = quiz_question[0].question_id
        else:
            # just a safe guard in case something went terribly wrong.
            return redirect('home_page')

    return redirect('question_view_page', quiz_id=quiz_id, question_id=question_id)
