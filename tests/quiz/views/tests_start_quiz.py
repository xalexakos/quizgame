from django.contrib.auth.models import User
from django.test import TestCase

from quiz.models import Quiz, Question, Answer, QuizQuestion, UserQuiz, UserQuizAnswer


class StartQuizTestCase(TestCase):
    def test_get(self):
        quiz = Quiz.objects.create()

        question_1 = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question_1.pk),
            Answer(text='Miami', question_id=question_1.pk),
            Answer(text='Washington DC', question_id=question_1.pk),
            Answer(text='Chicago', question_id=question_1.pk),
        ])

        question_2 = Question.objects.create(text='Which is the best programming language?')
        Answer.objects.bulk_create([
            Answer(text='Python', question_id=question_2.pk),
            Answer(text='Java', question_id=question_2.pk),
            Answer(text='Ruby', question_id=question_2.pk),
            Answer(text='Go', question_id=question_2.pk),
        ])

        question_3 = Question.objects.create(text='Which is the best music instrument?')
        Answer.objects.bulk_create([
            Answer(text='Piano', question_id=question_3.pk),
            Answer(text='Guitar', question_id=question_3.pk),
            Answer(text='Drums', question_id=question_3.pk),
            Answer(text='Bass', question_id=question_3.pk),
        ])

        QuizQuestion.objects.bulk_create([
            QuizQuestion(quiz_id=quiz.id, question_id=question_1.id, order=1),
            QuizQuestion(quiz_id=quiz.id, question_id=question_2.id, order=2),
            QuizQuestion(quiz_id=quiz.id, question_id=question_3.id, order=3)
        ])

        user = User.objects.create(username='testuser')
        self.client.force_login(user)

        self.assertEqual(UserQuiz.objects.filter(user_id=user.id).count(), 0)

        # start a new test.
        response = self.client.get('/quiz/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/quiz/%s/question/%s/' % (quiz.id, question_1.id))

        # validate the started quiz.
        user_quiz = UserQuiz.objects.get(user_id=user.id)
        self.assertEqual(user_quiz.quiz_id, quiz.id)

        # resume the test
        response = self.client.get('/quiz/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/quiz/%s/question/%s/' % (quiz.id, question_1.id))

        # validate the resumed quiz.
        user_quiz = UserQuiz.objects.get(user_id=user.id)
        self.assertEqual(user_quiz.quiz_id, quiz.id)

        # answer a question and try again.
        answer = Answer.objects.get(text='Washington DC', question_id=question_1.pk)
        UserQuizAnswer.objects.create(userquiz_id=user_quiz.id, question_id=question_1.pk, answer_id=answer.id)

        # resume the test
        response = self.client.get('/quiz/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/quiz/%s/question/%s/' % (quiz.id, question_2.id))
