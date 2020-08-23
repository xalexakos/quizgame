import json

from django.test import TestCase

from quiz.models import Quiz, Question, Answer, QuizQuestion


class QuizGameAPIViewTestCase(TestCase):
    def test_quiz_get(self):
        """ QuizGameAPIView get() method. """
        quiz = Quiz.objects.create()
        question = Question.objects.create(text='What is the capital of the United States?')
        Answer.objects.bulk_create([
            Answer(text='New York', question_id=question.pk),
            Answer(text='Miami', question_id=question.pk),
            Answer(text='Washington DC', question_id=question.pk, is_correct=True),
            Answer(text='Chicago', question_id=question.pk),
        ])

        QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question.id, order=1)

        with self.assertNumQueries(4):
            response = self.client.get('/api/quiz/')

        result = json.loads(response.content)
        self.assertEqual(list(result.keys()), ['id', 'questions'])
        self.assertEqual(result['id'], quiz.id)

        qs = result['questions']
        self.assertEqual(len(qs), 1)
        self.assertEqual(list(qs[0].keys()), ['id', 'text', 'answers'])

        self.assertEqual(qs[0]['id'], question.id)
        self.assertEqual(qs[0]['text'], 'What is the capital of the United States?')

        answers = qs[0]['answers']
        self.assertEqual(len(answers), 4)

        ans_qs = Answer.objects.all()
        self.assertEqual(answers[0]['id'], ans_qs[0].id)
        self.assertEqual(answers[0]['text'], 'New York')
        self.assertEqual(answers[1]['id'], ans_qs[1].id)
        self.assertEqual(answers[1]['text'], 'Miami')
        self.assertEqual(answers[2]['id'], ans_qs[2].id)
        self.assertEqual(answers[2]['text'], 'Washington DC')
        self.assertEqual(answers[3]['id'], ans_qs[3].id)
        self.assertEqual(answers[3]['text'], 'Chicago')
