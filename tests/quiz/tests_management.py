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
        call_command('createquizzes', '5', stdout=out)

        self.assertEqual(Question.objects.count(), 50)
        self.assertEqual(Answer.objects.count(), 200)
        self.assertEqual(Quiz.objects.count(), 5)
        self.assertEqual(QuizQuestion.objects.count(), 50)

        self.assertIn('Fetched a new list of questions.', out.getvalue())
        self.assertIn('Created quiz "1","2","3","4","5"', out.getvalue())

        # validate a random quiz
        quiz = Quiz.objects.first()
        questions = QuizQuestion.objects.filter(quiz_id=quiz.id).order_by('order')
        for i in range(10):
            self.assertEqual(questions[i].order, i + 1)
