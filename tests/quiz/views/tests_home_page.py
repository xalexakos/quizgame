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

        # table headers
        self.assertContains(response, '<th class="ht-quiz">Quiz</th>')
        self.assertContains(response, '<th class="ht-score">Score</th>')
        self.assertContains(response, '<th class="ht-rate">8+ answers</th>')
        self.assertContains(response, '<th class="ht-date">Completed at</th>')

        # table results
        self.assertContains(response, '<td class="ht-quiz">Quiz - 3</td>')
        self.assertContains(response, '<td class="ht-quiz">Quiz - 2</td>')
        self.assertContains(response, '<td class="ht-score">0 / 10</td>')
        self.assertContains(response, '<td class="ht-rate">0%</td>')
        self.assertContains(response, '<td class="ht-date">Aug. 2, 2020, 10 a.m.</td>')
        self.assertContains(response, '<td class="ht-date">Aug. 1, 2020, 10 a.m.</td>')
