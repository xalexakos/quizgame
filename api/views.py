from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QuizSerializer, SubmitQuizSerializer
from quiz.models import Quiz
from utils import calculate_perc, get_quiz_executions


class QuizGameAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        """ Fetch a random quiz. """
        quiz = Quiz.objects.random()
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        """ Submit a quiz. """
        serializer = SubmitQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(dict((k, v) for k, v in serializer.data.items() if k == 'correct_answers_no'))


class QuizGameSuccessRateAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request):
        """ Fetch a random quiz. """
        quizzes = Quiz.objects.all()

        response_data = [{
            'id': quiz.id,
            'success_rate': calculate_perc(*get_quiz_executions(quiz_id=quiz.id)) + '%'
        } for quiz in quizzes]

        return Response({'results': response_data})
