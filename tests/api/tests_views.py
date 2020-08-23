import json

from django.test import TestCase
from django.urls import reverse

from quiz.models import Quiz, Question, Answer, QuizQuestion


class QuizGameAPIViewTestCase(TestCase):
    view_name = 'quiz'

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
            response = self.client.get(reverse(self.view_name))
        self.assertEqual(response.status_code, 200)

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

    def test_quiz_post(self):
        """ QuizGameAPIView post() method. """
        quiz = Quiz.objects.create()
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

        with self.assertNumQueries(0):
            response = self.client.post(reverse(self.view_name), '{}', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'quiz': ['This field is required.'],
            'quiz_answers': ['This field is required.']
        })

        with self.assertNumQueries(0):
            response = self.client.post(reverse(self.view_name), json.dumps({'quiz': None, 'quiz_answers': []}),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'quiz': ['This field may not be null.'],
            'quiz_answers': {'non_field_errors': ['This list may not be empty.']}
        })

        quiz_answers = [
            {'question': question_1.id, 'answer': 0},
            {'question': question_2.id, 'answer': 'abc'},
            {'question': question_3.id, 'answer': None},
            {}
        ]
        with self.assertNumQueries(4):
            response = self.client.post(reverse(self.view_name),
                                        json.dumps({'quiz': quiz.id, 'quiz_answers': quiz_answers}),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'quiz_answers': [
                {'answer': ['Invalid answer id.']},
                {'answer': ['A valid integer is required.']},
                {'answer': ['This field may not be null.']},
                {'answer': ['This field is required.'], 'question': ['This field is required.']}
            ]
        })

        # missing question
        quiz_answers = [
            {'question': question_1.id,
             'answer': Answer.objects.get(text='Washington DC', question_id=question_1.pk).pk},
            {'question': question_3.id,
             'answer': Answer.objects.get(text='Bass', question_id=question_3.pk).pk}
        ]
        with self.assertNumQueries(6):
            response = self.client.post(reverse(self.view_name),
                                        json.dumps({'quiz': quiz.id, 'quiz_answers': quiz_answers}),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ['Some questions have not been sent. The required number of questions to be '
                                 'answered is 3']
        })

        # invalid question answer combination
        quiz_answers = [
            {'question': question_1.id,
             'answer': Answer.objects.get(text='Washington DC', question_id=question_1.pk).pk},
            {'question': question_2.id,
             'answer': Answer.objects.get(text='Washington DC', question_id=question_1.pk).pk},
            {'question': question_2.id,
             'answer': Answer.objects.get(text='Bass', question_id=question_3.pk).pk}
        ]
        with self.assertNumQueries(8):
            response = self.client.post(reverse(self.view_name),
                                        json.dumps({'quiz': quiz.id, 'quiz_answers': quiz_answers}),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ['Some questions have not been sent. The required number of questions to be '
                                 'answered is 3']
        })

        # submit a quiz with 2/3 correct answers.
        quiz_answers = [
            {'question': question_1.id,
             'answer': Answer.objects.get(text='Washington DC', question_id=question_1.pk).pk},
            {'question': question_2.id,
             'answer': Answer.objects.get(text='Java', question_id=question_2.pk).pk},
            {'question': question_3.id,
             'answer': Answer.objects.get(text='Guitar', question_id=question_3.pk).pk}
        ]
        with self.assertNumQueries(9):
            response = self.client.post(reverse(self.view_name),
                                        json.dumps({'quiz': quiz.id, 'quiz_answers': quiz_answers}),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'correct_answers_no': 2})
