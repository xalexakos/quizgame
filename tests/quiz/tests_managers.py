from django.test import TestCase

from quiz.models import Quiz


class QuizManagerTestCase(TestCase):
    def test_random(self):
        self.assertIsNone(Quiz.objects.random())

        q1 = Quiz.objects.create()
        q2 = Quiz.objects.create()
        q3 = Quiz.objects.create()

        with self.assertNumQueries(2):
            self.assertIn(Quiz.objects.random(), [q1, q2, q3])

        with self.assertNumQueries(2):
            self.assertEqual(Quiz.objects.random(exclude_ids=[q1.id, q2.id]), q3)