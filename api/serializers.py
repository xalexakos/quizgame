from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quiz.models import Quiz, Question, Answer, QuizQuestion


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'questions']


class QuizResultsSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True)

    @staticmethod
    def validate_question(value):
        try:
            Question.objects.get(id=value)
        except Question.DoesNotExist:
            raise ValidationError('Invalid question id.')

        return value

    @staticmethod
    def validate_answer(value):
        try:
            Answer.objects.get(id=value)
        except Answer.DoesNotExist:
            raise ValidationError('Invalid answer id.')

        return value


class SubmitQuizSerializer(serializers.Serializer):
    quiz = serializers.IntegerField(required=True)
    quiz_answers = QuizResultsSerializer(many=True, required=True, allow_empty=False)
    correct_answers_no = serializers.IntegerField(read_only=True)

    def validate(self, data):
        """
        Validate the number of questions answered.
        All questions must be answered in order to have a successful submission.
        """
        questions_no = QuizQuestion.objects.filter(quiz_id=data['quiz']).count()

        quiz_answers = data['quiz_answers']
        answers = Answer.objects.filter(id__in=[int(d['answer']) for d in quiz_answers],
                                        question_id__in=[int(d['question']) for d in quiz_answers])
        answers_count = answers.count()

        if answers_count != questions_no:
            raise ValidationError('Some questions have not been sent. '
                                  'The required number of questions to be answered is %s' % questions_no)

        data['correct_answers_no'] = answers.filter(is_correct=True).count()
        return data
