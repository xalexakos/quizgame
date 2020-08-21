from django.contrib.auth.models import User
from django.test import TestCase

from quiz.models import Quiz, Question, QuizQuestion, Answer


class QuestionViewPageTestCase(TestCase):
    def test_get(self):
        """ validate the question view page rendering. """
        quiz = Quiz.objects.create()
        question = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question.pk),
            Answer(text='Miami', question_id=question.pk),
            Answer(text='Washington DC', question_id=question.pk, is_correct=True),
            Answer(text='Chicago', question_id=question.pk),
        ])

        QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question.id, order=1)

        user = User.objects.create(username='testuser')
        self.client.force_login(user)

        response = self.client.get('/quiz/%s/question/%s/' % (quiz.pk, question.pk))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3>1 - What is the capital of the United States?</h3>')
        self.assertContains(response, '<input type="radio" name="answer" value="New York" /> New York <br /><br />')
        self.assertContains(response, '<input type="radio" name="answer" value="Miami" /> Miami <br /><br />')
        self.assertContains(response,
                            '<input type="radio" name="answer" value="Washington DC" /> Washington DC <br /><br />')
        self.assertContains(response, '<input type="radio" name="answer" value="Chicago" /> Chicago <br /><br />')
