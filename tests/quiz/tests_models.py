from unittest import TestCase

from quiz.models import Quiz


class QuizModelTestCase(TestCase):
    def test_unicode(self):
        quiz = Quiz.objects.create()
        self.assertEqual(quiz.__unicode__(), 'Quiz - %d' % quiz.pk)
