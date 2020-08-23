from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QuizSerializer, SubmitQuizSerializer
from quiz.models import Quiz


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
