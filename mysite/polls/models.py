import datetime

from django.db import models
from django.utils import timezone
"""Each model is being represented by a class which is a subclass of
models.Model. The variables of these classes are to become database field.
Each field is an instance of the some class Field which can be CharField,
EmailField, DateTimeField, and so on. Some can have required parameters.
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
