import json
import requests
from django.test import TestCase


class OpenTDBTestCase(TestCase):
    """ Opentdb api results schema validation. """

    def test_results_schema(self):
        response = requests.get('https://opentdb.com/api.php?amount=50&type=multiple')
        self.assertEqual(response.status_code, 200)

        # validate the response keys
        results = json.loads(response.content)
        self.assertEqual(list(results.keys()), ['response_code', 'results'])

        # validate the number of returned questions
        questions = results['results']
        self.assertEqual(len(questions), 50)

        # validate questions' structure.
        self.assertEqual(
            list(questions[0].keys()),
            ['category', 'type', 'difficulty', 'question', 'correct_answer', 'incorrect_answers']
        )

        self.assertEqual(type(questions[0]['category']), str)
        self.assertEqual(type(questions[0]['type']), str)
        self.assertEqual(type(questions[0]['difficulty']), str)
        self.assertEqual(type(questions[0]['question']), str)
        self.assertEqual(type(questions[0]['correct_answer']), str)
        self.assertEqual(type(questions[0]['incorrect_answers']), list)

        self.assertEqual(len(questions[0]['incorrect_answers']), 3)
        self.assertEqual(type(questions[0]['incorrect_answers'][0]), str)
