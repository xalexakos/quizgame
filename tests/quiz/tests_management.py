from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from quiz.models import Quiz, Question, Answer, QuizQuestion


class CreateQuizzesTestCase(TestCase):
    def test_command(self):
        """ Validate the creation of 100 quizzes. """
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)
        self.assertEqual(Quiz.objects.count(), 0)
        self.assertEqual(QuizQuestion.objects.count(), 0)

        out = StringIO()
        call_command('createquizzes', stdout=out)

        self.assertEqual(Question.objects.count(), 50)
        self.assertEqual(Answer.objects.count(), 200)
        self.assertEqual(Quiz.objects.count(), 100)
        self.assertEqual(QuizQuestion.objects.count(), 1000)

        self.assertIn('Fetching some questions.', out.getvalue())
        self.assertIn('100 new quizzes have been created.', out.getvalue())
