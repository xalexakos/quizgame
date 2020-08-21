from django.test import TestCase

from quiz.models import Quiz


class QuizManagerTestCase(TestCase):
    def test_random(self):
        self.assertIsNone(Quiz.objects.random())

        q1 = Quiz.objects.create()
        q2 = Quiz.objects.create()
        q3 = Quiz.objects.create()

        self.assertIn(Quiz.objects.random(), [q1, q2, q3])
