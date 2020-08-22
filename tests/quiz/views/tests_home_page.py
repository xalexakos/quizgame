from django.contrib.auth.models import User
from django.test import TestCase

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
