from unittest import TestCase

from quiz.models import Quiz, Question, Answer, QuizQuestion


class QuizModelTestCase(TestCase):
    def test_str(self):
        quiz = Quiz.objects.create()
        self.assertEqual(quiz.__str__(), 'Quiz - %d' % quiz.pk)


class QuestionModelTestCase(TestCase):
    def test_str(self):
        question = Question.objects.create(text='What is the capital of the United States?')
        self.assertEqual(question.__str__(), 'What is the capital of the United States?')


class AnswerModelTestCase(TestCase):
    def test_str(self):
        question = Question.objects.create(text='What is the capital of the United States?')
        answer = Answer.objects.create(question_id=question.id, text='Washington DC', is_correct=True)
        self.assertEqual(answer.__str__(), 'Washington DC')


class QuizQuestionModelTestCase(TestCase):
    def test_str(self):
        quiz = Quiz.objects.create()
        question = Question.objects.create(text='What is the capital of the United States?')
        quiz_question = QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question.id, order=3)
        self.assertEqual(quiz_question.__str__(), '3 - What is the capital of the United States?')
