from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from pytz import utc

from quiz.models import Quiz, UserQuiz
from utils import calculate_perc, get_quiz_executions, increment_quiz_success_rate, get_user_history


class QuizGameUtilsTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def test_calculate_perc(self):
        self.assertEqual(calculate_perc(1, 2), '50')
        self.assertEqual(calculate_perc(3, 9), '33.33')
        self.assertEqual(calculate_perc(1, 0), '0')

    def test_get_quiz_executions(self):
        quiz = Quiz.objects.create()

        with self.assertNumQueries(2):
            suc, tot = get_quiz_executions(quiz_id=quiz.id)

        self.assertEqual(suc, 0)
        self.assertEqual(tot, 0)

        with self.assertNumQueries(0):
            suc, tot = get_quiz_executions(quiz_id=quiz.id)

        self.assertEqual(suc, 0)
        self.assertEqual(tot, 0)

    def test_increment_quiz_success_rate(self):
        quiz = Quiz.objects.create()

        with self.assertNumQueries(2):
            increment_quiz_success_rate(quiz_id=quiz.id)

        with self.assertNumQueries(0):
            suc, tot = get_quiz_executions(quiz_id=quiz.id)

        self.assertEqual(suc, 0)
        self.assertEqual(tot, 1)

        with self.assertNumQueries(0):
            increment_quiz_success_rate(quiz_id=quiz.id, is_successful=True)

        with self.assertNumQueries(0):
            suc, tot = get_quiz_executions(quiz_id=quiz.id)

        self.assertEqual(suc, 1)
        self.assertEqual(tot, 2)

    def test_get_user_history(self):
        user = User.objects.create(username='testuser')

        quiz = Quiz.objects.create()
        quiz2 = Quiz.objects.create()
        UserQuiz.objects.create(user_id=user.id, quiz_id=quiz.id,
                                completed_at=datetime(2020, 8, 1, 10, 0, 0, tzinfo=utc))
        UserQuiz.objects.create(user_id=user.id, quiz_id=quiz2.id,
                                completed_at=datetime(2020, 8, 2, 10, 0, 0, tzinfo=utc))

        with self.assertNumQueries(2):
            user_history = get_user_history(user.id)

        self.assertEqual(user_history.count(), 2)

        with self.assertNumQueries(0):
            user_history = get_user_history(user.id)

        self.assertEqual(user_history.count(), 2)
