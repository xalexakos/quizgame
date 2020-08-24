from django.core.cache import cache
from django.test import TestCase

from quiz.models import Quiz
from utils import calculate_perc, get_quiz_executions, increment_quiz_success_rate


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
