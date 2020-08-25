from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import UniqueConstraint, Q

from quiz.managers import QuizManager


class Question(models.Model):
    text = models.TextField()
    submitted_answers = models.IntegerField(default=0)
    submitted_correct_answers = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    created = models.DateTimeField(auto_now_add=True)

    objects = QuizManager()

    def __str__(self):
        return 'Quiz - %d' % self.id


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

    class Meta:
        # a user can only have one running quiz.
        constraints = [
            UniqueConstraint(fields=['user'], condition=Q(completed_at__isnull=True),
                             name='unique_running_quiz_user')
        ]

    def __str__(self):
        return '%s' % self.quiz

    def save(self, *args, **kwargs):
        """ Delete the cached quiz history queryset. """
        super(UserQuiz, self).save(*args, **kwargs)
        cache.delete('uhq:%s' % self.user_id)


class UserQuizAnswer(models.Model):
    userquiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.answer
