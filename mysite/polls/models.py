import datetime

from django.db import models
from django.utils import timezone
"""Each model is being represented by a class which is a subclass of
models.Model. The variables of these classes are to become database field.
Each field is an instance of the some class Field which can be CharField,
EmailField, DateTimeField, and so on. Some can have required parameters.
"""


class Question(models.Model):

    # These become the attributes of the class.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """ Returns true if the pub_date is within a day"""
        now = timezone.now()
        # pub_date <= now means nothing that is in the future, or > now
        # and before hand yesterday(now-timedelta(day=1)) has to be <= pub_date
        # therefore if pub_date is less than it occurred longer than yesterday.
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # These are method attributes which help Django display on the admin
    # page.
    # be careful of the indent
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):

    # These become the attributes of the class.
    # The related_name is the same as default. I just wanted to show how to
    # rename the method made in Question. This is used in the template
    # detail.html.
    question = models.ForeignKey(Question, related_name='choice_set')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
