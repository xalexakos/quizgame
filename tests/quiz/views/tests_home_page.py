from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import utc

from quiz.models import Quiz, Answer, Question, UserQuiz, QuizQuestion


class HomePageTestCase(TestCase):
    def test_get(self):
        quiz = Quiz.objects.create()

        question_1 = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question_1.pk),
            Answer(text='Miami', question_id=question_1.pk),
            Answer(text='Washington DC', question_id=question_1.pk),
            Answer(text='Chicago', question_id=question_1.pk),
        ])
        QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question_1.id, order=1)

        user = User.objects.create(username='testuser')
        self.client.force_login(user)

        self.assertEqual(UserQuiz.objects.filter(user_id=user.id).count(), 0)

        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Start a random quiz')

        # start a quiz
        UserQuiz.objects.create(user_id=user.id, quiz_id=quiz.id)

        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '%s' % quiz)

        # validate history
        quiz = Quiz.objects.create()
        quiz2 = Quiz.objects.create()
        UserQuiz.objects.bulk_create([
            UserQuiz(user_id=user.id, quiz_id=quiz.id, completed_at=datetime(2020, 8, 1, 10, 0, 0, tzinfo=utc)),
            UserQuiz(user_id=user.id, quiz_id=quiz2.id, completed_at=datetime(2020, 8, 2, 10, 0, 0, tzinfo=utc))
        ])
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<tr><th>Quiz</th><th>Score</th><th>Completed</th></tr>')
        self.assertContains(response, '<tr><td style="width: 100px; text-align: left;">Quiz - 3</td>')
        self.assertContains(response, '<tr><td style="width: 100px; text-align: left;">Quiz - 2</td>')
        self.assertContains(response, '<td style="width: 50px; text-align: right;">0 / 10</td>')
        self.assertContains(response, '<td style="width: 250px; text-align: right;">Aug. 2, 2020, 10 a.m.</td>')
        self.assertContains(response, '<td style="width: 250px; text-align: right;">Aug. 1, 2020, 10 a.m.</td>')
