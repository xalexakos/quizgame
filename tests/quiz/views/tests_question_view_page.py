from django.contrib.auth.models import User
from django.test import TestCase

from quiz.models import Quiz, Question, QuizQuestion, Answer, UserQuiz, UserQuizAnswer


class QuestionViewPageTestCase(TestCase):
    def test_get(self):
        """ Validate the question view page rendering. """
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
        with self.assertNumQueries(5):
            response = self.client.get('/quiz/%s/question/%s/' % (quiz.pk, question.pk))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<h3>1 - What is the capital of the United States?</h3>')
        self.assertContains(response,
                            '<input type="radio" name="answer" value="New York" required /> New York <br /><br />')
        self.assertContains(response,
                            '<input type="radio" name="answer" value="Miami" required /> Miami <br /><br />')
        self.assertContains(
            response, '<input type="radio" name="answer" value="Washington DC" required /> Washington DC <br /><br />')
        self.assertContains(response,
                            '<input type="radio" name="answer" value="Chicago" required /> Chicago <br /><br />')

    def test_post(self):
        """ Answer some questions and validate the page's behavior. """
        quiz = Quiz.objects.create()

        user = User.objects.create(username='testuser')
        user_quiz = UserQuiz.objects.create(user_id=user.id, quiz_id=quiz.id)

        question_1 = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question_1.pk),
            Answer(text='Miami', question_id=question_1.pk),
            Answer(text='Washington DC', question_id=question_1.pk, is_correct=True),
            Answer(text='Chicago', question_id=question_1.pk),
        ])

        question_2 = Question.objects.create(text='Which is the best programming language?')
        Answer.objects.bulk_create([
            Answer(text='Python', question_id=question_2.pk, is_correct=True),
            Answer(text='Java', question_id=question_2.pk),
            Answer(text='Ruby', question_id=question_2.pk),
            Answer(text='Go', question_id=question_2.pk),
        ])

        question_3 = Question.objects.create(text='Which is the best music instrument?')
        Answer.objects.bulk_create([
            Answer(text='Piano', question_id=question_3.pk),
            Answer(text='Guitar', question_id=question_3.pk, is_correct=True),
            Answer(text='Drums', question_id=question_3.pk),
            Answer(text='Bass', question_id=question_3.pk),
        ])

        QuizQuestion.objects.bulk_create([
            QuizQuestion(quiz_id=quiz.id, question_id=question_1.id, order=1),
            QuizQuestion(quiz_id=quiz.id, question_id=question_2.id, order=2),
            QuizQuestion(quiz_id=quiz.id, question_id=question_3.id, order=3)
        ])

        self.client.force_login(user)

        # answer the first question correctly
        with self.assertNumQueries(11):
            response = self.client.post('/quiz/%s/question/%s/' % (quiz.pk, question_1.pk), {'answer': 'Washington DC'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Your answer "Washington DC" is <span class="success">correct</span>.</p>')

        user_quiz.refresh_from_db()
        self.assertEqual(user_quiz.correct_answers, 1)

        self.assertEqual(
            UserQuizAnswer.objects.filter(userquiz_id=user_quiz.id, answer__text='Washington DC').count(), 1
        )

        # attempt to answer the first question once more.
        with self.assertNumQueries(9):
            response = self.client.post('/quiz/%s/question/%s/' % (quiz.pk, question_1.pk), {'answer': 'Washington DC'})

        self.assertEqual(response.status_code, 200)

        user_quiz.refresh_from_db()
        self.assertEqual(user_quiz.correct_answers, 1)

        self.assertEqual(
            UserQuizAnswer.objects.filter(userquiz_id=user_quiz.id, answer__text='Washington DC').count(), 1
        )

        # answer the second question mistakenly.
        with self.assertNumQueries(10):
            response = self.client.post('/quiz/%s/question/%s/' % (quiz.pk, question_2.pk), {'answer': 'Java'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Your answer "Java" is <span class="has-error">wrong</span>.</p>')

        user_quiz.refresh_from_db()
        self.assertEqual(user_quiz.correct_answers, 1)

        self.assertEqual(
            UserQuizAnswer.objects.filter(userquiz_id=user_quiz.id, answer__text='Java').count(), 1
        )

    def test_post_final_question(self):
        """ Answer the last question and validate the page's behavior. """
        quiz = Quiz.objects.create()

        user = User.objects.create(username='testuser')
        user_quiz = UserQuiz.objects.create(user_id=user.id, quiz_id=quiz.id)

        question_1 = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question_1.pk),
            Answer(text='Miami', question_id=question_1.pk),
            Answer(text='Washington DC', question_id=question_1.pk, is_correct=True),
            Answer(text='Chicago', question_id=question_1.pk),
        ])

        QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question_1.id, order=10)

        self.client.force_login(user)

        # answer the last question correctly
        with self.assertNumQueries(11):
            response = self.client.post('/quiz/%s/question/%s/' % (quiz.pk, question_1.pk), {'answer': 'Washington DC'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Your answer "Washington DC" is <span class="success">correct</span>.</p>')
        self.assertContains(response, '<h3>The quiz has been completed.</h3>')
        self.assertContains(response, '<p>Your score is: <h2>1 / 10</h2></p>')
        self.assertContains(response, '<a href="/quiz/">Take another quiz</a>')
        self.assertContains(response, '<a href="/">Return to home page</a>')

        user_quiz.refresh_from_db()
        self.assertEqual(user_quiz.correct_answers, 1)

        self.assertEqual(
            UserQuizAnswer.objects.filter(userquiz_id=user_quiz.id, answer__text='Washington DC').count(), 1
        )
