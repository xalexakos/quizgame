import json
import math
import random
import requests

from django.conf import settings
from django.core.management import BaseCommand

from quiz.models import Quiz, Question, Answer, QuizQuestion


class Command(BaseCommand):
    help = """ Fetch new questions and create quizzes. 
    The command parameter defines the number of quizzes that will be created. 
    For every 5 quizzes new questions are fetched."""

    @staticmethod
    def _create_quiz(questions):
        """ Given a list of 10 questions create a quiz. """
        quiz = Quiz.objects.create()

        for i, r in enumerate(questions):
            question = Question.objects.filter(text=r['question'])

            if not question.exists():
                # import the question only if it is not already imported.
                question = Question.objects.create(text=r['question'])
                answers = [{'text': r['correct_answer'], 'is_correct': True, 'question_id': question.id}]

                for n in range(3):
                    answers.append({'text': r['incorrect_answers'][n], 'is_correct': False, 'question_id': question.id})

                random.shuffle(answers)

                for ans_kwargs in answers:
                    Answer.objects.create(**ans_kwargs)
            else:
                question = question[0]

            QuizQuestion.objects.create(quiz_id=quiz.id, question_id=question.id, order=i + 1)

        return quiz.id

    def add_arguments(self, parser):
        parser.add_argument('quizzes_no', nargs='+', type=int)

    def handle(self, *args, **options):
        quizzes_created = 0
        quizzes_no = int(options['quizzes_no'][0])

        for _ in range(math.ceil(quizzes_no / 5)):
            self.stdout.write(self.style.WARNING('Fetched a new list of questions.'))

            try:
                resp = requests.get(settings.OPENTDB_API_URL)
            except Exception:
                self.stderr.write(self.style.ERROR('Could not fetch the questions.'))
            else:
                results = json.loads(resp.content)['results']

                quizzes = []
                for questions in [results[i:i + 10] for i in range(0, len(results), 10)]:
                    if quizzes_created < quizzes_no:
                        quizzes.append(self._create_quiz(questions=questions))
                    quizzes_created += 1

                self.stdout.write('Created quiz %s' % ','.join(['"%s"' % q for q in quizzes]))
