from django.test import TestCase

from utils import calculate_perc


class QuizGameUtilsTestCase(TestCase):
    def test_calculate_perc(self):
        self.assertEqual(calculate_perc(1, 2), '50')
        self.assertEqual(calculate_perc(3, 9), '33.33')
        self.assertEqual(calculate_perc(1, 0), '0')
