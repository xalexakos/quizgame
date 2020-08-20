import json
import random
import requests

from django.conf import settings
from django.core.management import BaseCommand

from quiz.models import Quiz, Question, Answer, QuizQuestion


class Command(BaseCommand):
    help = 'Fetch 50 new questions and create 100 new quizzes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Fetching some questions.'))

        try:
            resp = requests.get(settings.OPENTDB_API_URL)
        except Exception:
            self.stderr.write(self.style.ERROR('Fetching some questions.'))
        else:
            results = json.loads(resp.content)['results']

            # save questions and answers
            imported_questions = []
            for r in results:
                # todo: mind in texts the symbols such as '"' or "<" or even "&" to be correctly imported in db.
                q = Question.objects.filter(text=r['question'])
                if not q.exists():
                    # import the question only if it is not already imported.
                    q = Question.objects.create(text=r['question'])
                    Answer.objects.create(question=q, text=r['correct_answer'], is_correct=True)
                    Answer.objects.create(question=q, text=r['incorrect_answers'][0])
                    Answer.objects.create(question=q, text=r['incorrect_answers'][1])
                    Answer.objects.create(question=q, text=r['incorrect_answers'][2])

                imported_questions.append(q.id)

            # todo: not the best randomizer ever created. improve this later on.
            # create 100 new quizzes.
            for i in range(100):
                quiz = Quiz.objects.create()

                quiz_questions = []
                selected_questions = random.sample(imported_questions, 10)
                for j in range(10):
                    quiz_questions.append(
                        QuizQuestion(quiz_id=quiz.id, question_id=selected_questions[j], order=j + 1)
                    )

                QuizQuestion.objects.bulk_create(quiz_questions)

            self.stdout.write(self.style.SUCCESS('100 new quizzes have been created.'))
