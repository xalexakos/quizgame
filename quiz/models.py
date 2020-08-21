from django.contrib.auth.models import User
from django.db import models

from quiz.managers import QuizManager


class Quiz(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    objects = QuizManager()

    def __str__(self):
        return 'Quiz - %d' % self.id


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(choices=[(i + 1, i + 1) for i in range(10)], default=0)

    def __str__(self):
        return '%s - %s' % (self.order, self.question)


class UserQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True)
    correct_answers = models.IntegerField(choices=[(i + 1, i + 1) for i in range(10)], default=0)

    def __str__(self):
        return '%s' % self.quiz


class UserQuizAnswer(models.Model):
    userquiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.answer
