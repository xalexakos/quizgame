from django.db import models
from django.db.models.aggregates import Count
from random import randint


class QuizManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        if not count:
            return

        random_index = randint(0, count - 1)
        return self.all()[random_index]
