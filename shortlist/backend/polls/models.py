import datetime as dt

from django.utils import timezone
from django.contrib import admin
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return "Q{:02d}-{}".format(self.id, self.question_text)

    @admin.display(boolean=True, ordering="pub_date", description="Published Recently?")
    def was_published_recently(self):
        upper = timezone.now()
        lower = upper - dt.timedelta(days=1)
        return lower <= self.pub_date <= upper


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
