from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QuizSerializer
from quiz.models import Quiz


# todo: test me.
class QuizGameAPIView(APIView):

    def get(self, request):
        quiz = Quiz.objects.random()
        serializer = QuizSerializer(quiz)

        return Response(serializer.data)
