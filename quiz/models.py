from django.db import models


class Quiz(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Quiz - %d' % self.id


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
