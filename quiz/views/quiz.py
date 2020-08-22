from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.timezone import now

from quiz.models import Answer, QuizQuestion, UserQuiz, Quiz, UserQuizAnswer


@login_required(login_url='login_page')
def question_view_page(request, quiz_id, question_id):
    """ Renders a question with its related answers. """
    try:
        quiz_question = QuizQuestion.objects.get(quiz_id=quiz_id, question_id=question_id)
    except QuizQuestion.DoesNotExist:
        return redirect('home_page')
    else:
        answers = Answer.objects.filter(question_id=quiz_question.question_id)

    question = quiz_question.question
    context = {
        'quiz_id': quiz_id,
        'question_no': quiz_question.order,
        'question': question.text,
        'answers': answers.values('text', 'is_correct')
    }

    if request.method == 'POST':
        # the user has submitted an answer.
        user_quiz = UserQuiz.objects.get(quiz_id=quiz_id, user_id=request.user.id)
        answer = answers.get(text=request.POST.get('answer'))

        uqa_kwargs = {
            'question_id': quiz_question.question_id,
            'userquiz_id': user_quiz.id,
            'answer_id': answer.id
        }

        if not UserQuizAnswer.objects.filter(**uqa_kwargs).exists():
            # register the users answer.
            # the extra check is required to avoid registering the same answer twice.
            UserQuizAnswer.objects.create(**uqa_kwargs)
            question.submitted_answers = F('submitted_answers') + 1

            if answer.is_correct:
                # count the correct answer
                question.submitted_correct_answers = F('submitted_correct_answers') + 1

                # keep count of the quiz score.
                user_quiz.correct_answers += 1
                user_quiz.save()

            question.save()
            question.refresh_from_db()

        sr = str((question.submitted_correct_answers / question.submitted_answers) * 100)
        context.update({
            'submitted_answer': True,
            'is_correct': answer.is_correct,
            'user_answer': answer.text,
            'correct_answer': answers.filter(is_correct=True).first().text,
            'success_ratio': sr.rstrip('0').rstrip('.') if '.' in sr else sr
        })

        if quiz_question.order < 10:
            # the user has not completed the test yet.
            # include the next question url into the context.
            next_question = QuizQuestion.objects.filter(quiz_id=quiz_id, order=quiz_question.order + 1) \
                .values('question_id').first()
            context.update({'next_question': '/quiz/%s/question/%s/' % (quiz_id, next_question['question_id'])})
        else:
            # the quiz has been completed.
            # display the score.
            user_quiz.completed_at = now()
            user_quiz.save()

            context.update({'score': user_quiz.correct_answers})

    return render(request, 'quiz/quiz.html', context)


@login_required(login_url='login_page')
def start_quiz(request):
    """ Starts a new quest or populate the next question of an ongoing one. """
    try:
        user_quiz = UserQuiz.objects.get(completed_at__isnull=True, user_id=request.user.id)
    except UserQuiz.DoesNotExist:
        completed_quizzes = UserQuiz.objects.filter(user_id=request.user.id).values_list('quiz_id')
        quiz = Quiz.objects.random(completed_quizzes)

        if not quiz:
            # no quizzes where found so stay on home page forever.
            return redirect('home_page')

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
